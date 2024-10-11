import numpy as np
import pyvista as pv
import argparse
import os
from sklearn.neighbors import LocalOutlierFactor


def remove_outliers(points, contamination=0.2):
    lof = LocalOutlierFactor(n_neighbors=20, contamination=contamination)
    is_inlier = lof.fit_predict(points) > 0
    filtered_points = points[is_inlier]
    return filtered_points


def reconstruct_surface(input_file, output_file, contamination=0.1):
    # 读取点云数据
    points = np.loadtxt(input_file)

    # 移除异常值
    filtered_points = remove_outliers(points, contamination)

    # 创建一个 PolyData 对象
    point_cloud = pv.PolyData(filtered_points)

    # 使用 Delaunay 3D 三角化进行表面重建
    surface = point_cloud.delaunay_3d()

    # 保存重建的表面为 VTK 文件
    surface.save(output_file)
    print(f"Reconstructed surface and saved to {output_file}")


def process_directory(input_dir, output_dir, contamination=0.1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(300):
        input_file = os.path.join(input_dir, f'surface_points_{i}.txt')
        output_file = os.path.join(output_dir, f'surface_{i}.vtk')

        if os.path.exists(input_file):
            reconstruct_surface(input_file, output_file, contamination)
        else:
            print(f"File {input_file} does not exist.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Reconstruct surface from point cloud files in a directory by removing outliers")
    parser.add_argument('input_dir', help="Path to input directory containing TXT files with point cloud data.")
    parser.add_argument('output_dir', help="Path to output directory to save the reconstructed surfaces.")
    parser.add_argument('--contamination', type=float, default=0.1,
                        help="The amount of contamination of the data set, i.e., the proportion of outliers in the data set.")
    args = parser.parse_args()

    process_directory(args.input_dir, args.output_dir, args.contamination)
