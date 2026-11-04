#!/usr/bin/env python3
"""Generate a low-poly red sedan-shaped GLB matching the supplied reference.

Usage:
    python3 generate_cra_glb.py

This writes a file named `cra.glb` next to this script.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import trimesh

OUTPUT_PATH = Path(__file__).with_name("cra.glb")


def colorize(mesh: trimesh.Trimesh, rgba: tuple[float, float, float, float]) -> trimesh.Trimesh:
    rgba_arr = np.array(rgba, dtype=np.float64)
    mesh.visual.face_colors = np.tile(rgba_arr, (len(mesh.faces), 1))
    return mesh


def add_box(scene: trimesh.Scene, size: tuple[float, float, float], center: tuple[float, float, float], rgba: tuple[float, float, float, float]) -> None:
    mesh = trimesh.creation.box(extents=size)
    mesh.apply_translation(center)
    colorize(mesh, rgba)
    scene.add_geometry(mesh)


def add_wheel(scene: trimesh.Scene, center: tuple[float, float, float], radius: float = 0.32, width: float = 0.18) -> None:
    wheel = trimesh.creation.cylinder(radius=radius, height=width, sections=24)
    wheel.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    wheel.apply_translation(center)
    colorize(wheel, (0.1, 0.1, 0.1, 1.0))
    scene.add_geometry(wheel)


def build_car() -> trimesh.Scene:
    scene = trimesh.Scene()

    # Main body shell
    add_box(scene, (3.9, 1.72, 0.70), (0.0, 0.0, 0.52), (0.88, 0.06, 0.06, 1.0))

    # Roof/cabin glass
    add_box(scene, (2.1, 1.30, 0.56), (0.15, 0.0, 1.04), (0.18, 0.22, 0.27, 0.75))

    # Hood and trunk transitions
    add_box(scene, (1.0, 1.58, 0.22), (1.70, 0.0, 0.66), (0.85, 0.07, 0.07, 1.0))
    add_box(scene, (0.95, 1.52, 0.22), (-1.60, 0.0, 0.68), (0.84, 0.08, 0.08, 1.0))

    # Front grille / bumper block
    add_box(scene, (0.20, 1.12, 0.27), (2.08, 0.0, 0.32), (0.08, 0.08, 0.08, 1.0))

    # Rear light bar
    add_box(scene, (0.10, 1.12, 0.15), (-2.08, 0.0, 0.88), (0.92, 0.20, 0.10, 1.0))

    # Lower side trim
    add_box(scene, (3.5, 0.12, 0.12), (0.0, 0.82, 0.15), (0.11, 0.11, 0.11, 1.0))
    add_box(scene, (3.5, 0.12, 0.12), (0.0, -0.82, 0.15), (0.11, 0.11, 0.11, 1.0))

    # Wheel arches (simple side blocks to suggest the body contour)
    add_box(scene, (1.1, 0.08, 0.45), (1.05, 0.92, 0.35), (0.88, 0.06, 0.06, 1.0))
    add_box(scene, (1.1, 0.08, 0.45), (1.05, -0.92, 0.35), (0.88, 0.06, 0.06, 1.0))
    add_box(scene, (1.1, 0.08, 0.45), (-1.15, 0.92, 0.35), (0.88, 0.06, 0.06, 1.0))
    add_box(scene, (1.1, 0.08, 0.45), (-1.15, -0.92, 0.35), (0.88, 0.06, 0.06, 1.0))

    # Wheels
    wheel_positions = [
        (-1.20, 0.94, 0.34),
        (-1.20, -0.94, 0.34),
        (1.18, 0.94, 0.34),
        (1.18, -0.94, 0.34),
    ]
    for pos in wheel_positions:
        add_wheel(scene, pos)

    return scene


def main() -> None:
    car = build_car()
    export_path = str(OUTPUT_PATH)
    car.export(export_path)
    print(f"Created {export_path}")


if __name__ == "__main__":
    main()
