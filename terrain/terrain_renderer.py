from email.mime import image
from turtle import distance, heading, width
from unittest import result
from PIL import Image
from matplotlib.pyplot import grid
from PySide6.QtCore import QTimer

import numpy as np
import pyvista as pv
import rasterio

from pyproj import Transformer
from pyvistaqt import QtInteractor

class TerrainRenderer:

    def __init__(self, terrain, parent=None):
        self.fov_frames = []
        self.fov_index = 0

        self.fov_timer = QTimer()
        self.fov_timer.timeout.connect(self.next_fov_frame)
        self.terrain = terrain

        # -----------------------------
        # PyVista Widget
        # -----------------------------
        self.plotter = QtInteractor(parent)
        self.plotter.set_background("white")

        # -----------------------------
        # Terrain Parameters
        # -----------------------------
        # Terrain Parameters
        self.step = 8
        self.z_scale = 5.0
        self.marker_height = 500

        # FOV display range (only visualization)
        self.fov_display_range = 50000

        # Marker sizes
        self.sensor_radius = 1000
        self.target_radius = 1500

        # Coordinate conversion
        self.transformer = Transformer.from_crs(
            "EPSG:4326",
            terrain.crs,
            always_xy=True,
        )

        # -----------------------------
        # Actors
        # -----------------------------
        self.sensor_actors = {}
        self.target_actors = {}

        self.sensor_labels = {}
        self.target_labels = {}

        # Static trajectory
        self.trajectory_actor = None

        # Animation trail
        self.trail_points = []
        self.trail_actor = None
        # -----------------------------
        # FOV
        # -----------------------------
        self.fov_actor = None
        self.fov_mesh = None

        # Camera follow
        self.follow_target = True

        # Build terrain
        self.create_scene()

    # -------------------------------------------------

    def widget(self):

        return self.plotter
        # -------------------------------------------------

    def create_scene(self):

        # ----------------------------------------
        # DEM
        # ----------------------------------------

        elevation = self.terrain.elevation

        elevation = elevation[
            :: self.step,
            :: self.step,
        ]

        rows, cols = elevation.shape

        transform = self.terrain.transform

        # ----------------------------------------
        # Build mesh using raster transform
        # ----------------------------------------

        col, row = np.meshgrid(
            np.arange(cols),
            np.arange(rows),
        )

        x = transform.c + col * transform.a * self.step + row * transform.b

        y = transform.f + col * transform.d + row * transform.e * self.step

        z = elevation * self.z_scale

        grid = pv.StructuredGrid(
            x,
            y,
            z,
        )

        grid["Elevation"] = z.ravel(order="F")
        texture_img = Image.open("terrain/texture.png")

        texture = pv.numpy_to_texture(np.array(texture_img))

        # ----------------------------------------
        # Draw terrain
        # ----------------------------------------

        grid.texture_map_to_plane(inplace=True)

        self.plotter.add_mesh(grid, texture=texture)

        self.plotter.add_scalar_bar(title="Elevation (m)")

        self.plotter.show_axes()

        self.plotter.show_grid()

        # ----------------------------------------
        # Camera
        # ----------------------------------------

        self.plotter.view_isometric()

        self.plotter.camera.zoom(1.2)

        self.plotter.camera_position = "iso"

        camera = self.plotter.camera
        # camera.roll = 12
        camera.azimuth = 200
        self.plotter.render()

    def get_world_coordinates(
        self,
        latitude,
        longitude,
    ):
        """
        Convert Latitude/Longitude to DEM CRS coordinates.
        """

        x, y = self.transformer.transform(
            longitude,
            latitude,
        )

        return x, y

    # -------------------------------------------------

    def get_elevation(
        self,
        latitude,
        longitude,
    ):
        """
        Returns:
            x,
            y,
            terrain elevation
        """

        x, y = self.get_world_coordinates(
            latitude,
            longitude,
        )

        try:

            row, col = rasterio.transform.rowcol(
                self.terrain.transform,
                x,
                y,
            )

        except Exception:

            return None

        if (
            row < 0
            or row >= self.terrain.elevation.shape[0]
            or col < 0
            or col >= self.terrain.elevation.shape[1]
        ):
            return None

        terrain_height = float(self.terrain.elevation[row, col])

        if np.isnan(terrain_height):
            return None

        return (
            x,
            y,
            terrain_height,
        )
        # -------------------------------------------------

    def add_sensor(
        self,
        name,
        latitude,
        longitude,
        altitude=0,
    ):

        # Avoid duplicate sensors
        if name in self.sensor_actors:
            return

        result = self.get_elevation(
            latitude,
            longitude,
        )

        if result is None:

            print(f"Sensor '{name}' outside DEM")

            return

        x, y, terrain_z = result

        z = terrain_z * self.z_scale + self.marker_height + altitude

        sphere = pv.Sphere(
            radius=self.sensor_radius,
            center=(x, y, z),
        )

        actor = self.plotter.add_mesh(
            sphere,
            color="blue",
            smooth_shading=True,
            ambient=0.6,
            diffuse=0.9,
            specular=0.3,
        )

        label = self.plotter.add_point_labels(
            [(x, y, z + 2500)],
            [name],
            point_size=0,
            font_size=14,
            text_color="blue",
        )

        self.sensor_actors[name] = actor
        self.sensor_labels[name] = label

        self.plotter.render()

        print(f"Sensor Added : {name}")
        # -------------------------------------------------

    def add_target(
        self,
        name,
        latitude,
        longitude,
        altitude=0,
    ):

        # Don't create duplicate targets
        if name in self.target_actors:
            return

        result = self.get_elevation(
            latitude,
            longitude,
        )

        if result is None:

            print(f"Target '{name}' outside DEM")

            return

        x, y, terrain_z = result

        z = terrain_z * self.z_scale + self.marker_height + altitude

        sphere = pv.Sphere(
            radius=self.target_radius,
            center=(x, y, z),
        )

        actor = self.plotter.add_mesh(
            sphere,
            color="red",
            smooth_shading=True,
            ambient=0.7,
            diffuse=1.0,
            specular=0.5,
        )

        label = self.plotter.add_point_labels(
            [(x, y, z + 2500)],
            [name],
            point_size=0,
            font_size=14,
            text_color="red",
        )

        self.target_actors[name] = actor
        self.target_labels[name] = label

        self.plotter.render()

        print(f"Target Added : {name}")

    # -------------------------------------------------

    def move_target(
        self,
        name,
        latitude,
        longitude,
        altitude,
    ):

        result = self.get_elevation(
            latitude,
            longitude,
        )

        if result is None:
            return

        x, y, terrain_z = result

        # Target flies above terrain
        z = terrain_z * self.z_scale + self.marker_height + altitude

        # ---------------------------------------
        # Create target if it doesn't exist
        # ---------------------------------------

        if name not in self.target_actors:

            self.add_target(
                name,
                latitude,
                longitude,
            )

        # ---------------------------------------
        # Move target smoothly
        # ---------------------------------------

        actor = self.target_actors[name]

        sphere = pv.Sphere(
            radius=self.target_radius,
            center=(x, y, z),
        )

        actor.mapper.SetInputData(sphere)

        # ---------------------------------------
        # Update Label
        # ---------------------------------------

        if name in self.target_labels:

            self.plotter.remove_actor(self.target_labels[name])

        self.target_labels[name] = self.plotter.add_point_labels(
            [(x, y, z + 2500)],
            [name],
            point_size=0,
            font_size=14,
            text_color="red",
        )

        # ---------------------------------------
        # Add trail point
        # ---------------------------------------

        self.trail_points.append([x, y, z])

        if len(self.trail_points) >= 2:

            line = pv.lines_from_points(np.array(self.trail_points))

            if self.trail_actor is not None:

                self.plotter.remove_actor(self.trail_actor)

            self.trail_actor = self.plotter.add_mesh(
                line,
                color="yellow",
                line_width=6,
            )

        # ---------------------------------------
        # Camera Follow
        # ---------------------------------------

        if self.follow_target:

            self.plotter.set_focus((x, y, z))

        self.plotter.render()

        print(
            "Moving Target:",
            latitude,
            longitude,
            altitude,
        )

    # -------------------------------------------------
    # Draw complete trajectory path
    # -------------------------------------------------

    def draw_trajectory(
        self,
        trajectory_points,
    ):

        if len(trajectory_points) < 2:
            return

        points_3d = []

        for point in trajectory_points:

            latitude = point.latitude
            longitude = point.longitude
            altitude = point.alt

            result = self.get_elevation(latitude, longitude)

            if result is None:
                continue

            x, y, terrain_z = result

            z = terrain_z * self.z_scale + self.marker_height + altitude

            points_3d.append([x, y, z])

        if len(points_3d) < 2:
            return

        # remove old trajectory

        if hasattr(self, "trajectory_actor"):

            if self.trajectory_actor is not None:

                self.plotter.remove_actor(self.trajectory_actor)

        line = pv.lines_from_points(np.array(points_3d))

        self.trajectory_actor = self.plotter.add_mesh(
            line,
            color="orange",
            line_width=4,
        )

        self.plotter.render()

        print("3D trajectory drawn:", len(points_3d), "points")

    # -------------------------------------------------
    # Reset target animation
    # ------------------------------------------------

    def reset_animation(self):

        # Remove trail

        self.trail_points = []

        if self.trail_actor is not None:

            self.plotter.remove_actor(self.trail_actor)

            self.trail_actor = None

        # Remove target labels

        for label in self.target_labels.values():

            self.plotter.remove_actor(label)

        self.target_labels = {}

        # Remove target objects

        for actor in self.target_actors.values():

            self.plotter.remove_actor(actor)

        self.target_actors = {}

        self.plotter.render()

        print("3D Animation Reset")

    def plot_fov(self, frame):

    # remove previous pyramid
       # if self.fov_actor is not None:
        #    #self.plotter.remove_actor(self.fov_actor)
         #   self.fov_actor = None

    # -----------------------------
    # Sensor position
    # -----------------------------

        result = self.get_elevation(
            frame["sensor_lat"],
            frame["sensor_lon"]
        )

        if result is None:
            print("Sensor outside DEM")
            return

        sx, sy, terrain_z = result

        sensor_alt = float(
            frame.get("sensor_alt",0)
        )

        apex = np.array([
            sx,
        sy,
        terrain_z*self.z_scale
        + self.marker_height
        + sensor_alt
    ])

    # -----------------------------
    # Sensor + Target
    # -----------------------------

        self.add_sensor(
        frame.get("sensor_name","SENSOR"),
        frame["sensor_lat"],
        frame["sensor_lon"],
        sensor_alt
    )

        self.move_target(
        frame.get("target_name","TARGET"),
        frame["target_lat"],
        frame["target_lon"],
        frame.get("target_alt",0)
    )


    # -----------------------------
    # FOV INPUTS
    # -----------------------------

        azimuth=np.radians(
        float(frame["azimuth"])
    )

        elevation_value = float(frame["elevation"])

# Do not allow negative look angle
        if elevation_value < 0:
            elevation_value = 0

        elevation = np.radians(elevation_value)

        horizontal_fov=np.radians(
        float(frame.get("fov",22))
    )

        vertical_fov=np.radians(
        float(frame.get("vertical_fov",22))
    )

    # REAL RANGE
        real_range=float(
        frame.get("range",500000)
    )

    # TEST DISPLAY
        depth=min(
        real_range,
        50000
    )

    # -----------------------------
    # Direction vector
    # -----------------------------

        direction=np.array([

        np.sin(azimuth)
        *np.cos(elevation),

        np.cos(azimuth)
        *np.cos(elevation),

        np.sin(elevation)

    ])

        direction/=np.linalg.norm(direction)


    # -----------------------------
    # Mentor formula
    # -----------------------------

        far_center = (
        apex +
        direction*depth
    )

        half_width = (
        depth *
        np.tan(horizontal_fov/2)
    )

        half_height = (
        depth *
        np.tan(vertical_fov/2)
    )


    # -----------------------------
    # Camera coordinate system
    # -----------------------------

        right=np.array([

        np.cos(azimuth),
        -np.sin(azimuth),
        0

    ])

        up=np.cross(
        right,
        direction
    )

        up/=np.linalg.norm(up)


    # -----------------------------
    # 4 far vertices
    # -----------------------------

        top_right = (
        far_center
        + right*half_width
        + up*half_height
    )

        top_left = (
        far_center
        - right*half_width
        + up*half_height
    )

        bottom_left = (
        far_center
        - right*half_width
        - up*half_height
    )

        bottom_right = (
        far_center
        + right*half_width
        - up*half_height
    )


        vertices=np.array([

        apex,
        top_right,
        top_left,
        bottom_left,
        bottom_right

    ])


    # -----------------------------
    # Pyramid faces
    # -----------------------------

        faces=np.hstack([

        # far rectangle
        [4,1,2,3,4],

        # sides
        [3,0,1,2],
        [3,0,2,3],
        [3,0,3,4],
        [3,0,4,1]

    ])


     # create mesh only once
        if self.fov_mesh is None:

            self.fov_mesh = pv.PolyData(
            vertices,
            faces
        )

            self.fov_actor = self.plotter.add_mesh(
            self.fov_mesh,
            color="cyan",
            opacity=0.35,
            show_edges=True
        )

        else:

    # smooth update
          
    # update existing pyramid smoothly
            self.fov_mesh.points = vertices

    # notify VTK that geometry changed
        self.fov_mesh.Modified()

        self.fov_actor.mapper.Update()

        self.plotter.render()


        print("================")
        print("FOV PYRAMID")
        print("REAL RANGE:",real_range)
        print("DISPLAY RANGE:",depth)
        print("VERTICES:")
        print(vertices)
        print("================")
    def create_fov_actor(self):

        vertices = np.zeros((5,3))

        faces=np.hstack([

        [4,1,2,3,4],
        [3,0,1,2],
        [3,0,2,3],
        [3,0,3,4],
        [3,0,4,1]

        ])

        self.fov_mesh = pv.PolyData(
            vertices,
            faces
        )

        self.fov_actor = self.plotter.add_mesh(
        self.fov_mesh,
        color="cyan",
        opacity=0.35,
        show_edges=True
    )

    def start_fov_animation(self, frames):

        self.fov_frames = frames
        self.fov_index = 0

        self.fov_timer.start(100)

    def next_fov_frame(self):

        if self.fov_index >= len(self.fov_frames):
            self.fov_timer.stop()
            return

        frame = self.fov_frames[self.fov_index]

        self.plot_fov(frame)

        self.fov_index += 1

