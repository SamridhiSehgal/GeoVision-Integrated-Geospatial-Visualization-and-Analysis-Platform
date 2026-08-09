import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from pyproj import Transformer
import rasterio

class TerrainRenderer:

    def __init__(self, terrain, parent=None):

        self.terrain = terrain
        self.plotter = QtInteractor(parent)

        # Background
        self.plotter.set_background("white")

        # Rendering parameters
        self.step = 8  # Downsample
        self.z_scale = 5.0  # Vertical exaggeration
        # Convert GPS (Lat/Lon) → DEM CRS
        self.transformer = Transformer.from_crs(
            "EPSG:4326",
            self.terrain.crs,
            always_xy=True,
    )

        # Store actors
        self.sensor_actors = {}
        self.target_actors = {}
        self.create_scene()

    # -----------------------------------------------------

    def widget(self):
        return self.plotter

    # -----------------------------------------------------

    def create_scene(self):

        elevation = self.terrain.elevation.copy()

        # Uncomment ONLY if your DEM orientation is wrong

        # elevation = np.flipud(elevation)
        elevation = np.fliplr(elevation)
        # elevation = np.flipud(np.fliplr(elevation))

        # ----------------------------
        # Downsample
        # ----------------------------

        elevation = elevation[:: self.step, :: self.step]

        rows, cols = elevation.shape

        dx = self.terrain.resolution[0] * self.step
        dy = self.terrain.resolution[1] * self.step

        x = np.arange(cols) * dx
        y = np.arange(rows) * dy

        xx, yy = np.meshgrid(x, y)

        # ----------------------------
        # Height
        # ----------------------------

        zz = elevation * self.z_scale

        # ----------------------------
        # Structured Grid
        # ----------------------------

        grid = pv.StructuredGrid(xx, yy, zz)

        grid["Elevation"] = zz.ravel(order="F")

        # ----------------------------
        # Terrain
        # ----------------------------

        self.plotter.add_mesh(
            grid,
            scalars="Elevation",
            cmap="terrain",
            smooth_shading=True,
            show_edges=False,
            specular=0.15,
            ambient=0.30,
            diffuse=0.80,
        )

        # ----------------------------
        # Scalar Bar
        # ----------------------------

        self.plotter.add_scalar_bar(
            title="Elevation (m)",
            vertical=True,
            fmt="%.0f",
        )

        # ----------------------------
        # Axes
        # ----------------------------

        self.plotter.show_axes()

        self.plotter.show_grid()

        # ----------------------------
        # Camera
        # ----------------------------

        self.plotter.camera_position = "iso"

        self.plotter.reset_camera()

        self.plotter.render()

    # -----------------------------------------------------
    # -----------------------------------------------------


def get_world_coordinates(self, latitude, longitude):

    # Convert GPS to DEM CRS
    x, y = self.transformer.transform(longitude, latitude)

    # Convert world coordinates to raster row/column
    row, col = rasterio.transform.rowcol(self.terrain.transform, x, y)

    # Outside DEM
    if (
        row < 0
        or row >= self.terrain.elevation.shape[0]
        or col < 0
        or col >= self.terrain.elevation.shape[1]
    ):
        return None

    # DEM height
    z = self.terrain.elevation[row, col]

    return x, y, z

    def reset_camera(self):

        self.plotter.camera_position = "iso"
        self.plotter.reset_camera()
        self.plotter.render()

    # -----------------------------------------------------

    def clear_scene(self):

        self.plotter.clear()
        self.create_scene()
    # -----------------------------------------------------


def add_sensor(
    self,
    name,
    latitude,
    longitude,
):

    result = self.get_world_coordinates(
        latitude,
        longitude,
    )

    if result is None:
        return

    x, y, z = result

    sphere = pv.Sphere(radius=5000, center=(x, y, z * self.z_scale + 3000))

    actor = self.plotter.add_mesh(sphere, color="blue")

    self.plotter.add_point_labels(
        [(x, y, z * self.z_scale + 9000)],
        [name],
        point_size=0,
        font_size=16,
    )

    self.sensor_actors[name] = actor

    self.plotter.render()
    # -----------------------------------------------------


def add_target(
    self,
    name,
    latitude,
    longitude,
):

    result = self.get_world_coordinates(
        latitude,
        longitude,
    )

    if result is None:
        return

    x, y, z = result

    sphere = pv.Sphere(radius=5000, center=(x, y, z * self.z_scale + 3000))

    actor = self.plotter.add_mesh(sphere, color="red")

    self.plotter.add_point_labels(
        [(x, y, z * self.z_scale + 9000)],
        [name],
        point_size=0,
        font_size=16,
    )

    self.target_actors[name] = actor

    self.plotter.render()
