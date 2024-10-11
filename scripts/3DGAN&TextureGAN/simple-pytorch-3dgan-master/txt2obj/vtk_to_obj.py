#!/usr/bin/env python
import os
import pyvista as pv
import argparse


def convertFiles(indir, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    files = os.listdir(indir)
    files = [os.path.join(indir, f) for f in files if f.endswith('.vtk')]
    ret = 0
    print("In:", indir)
    print("Out:", outdir)
    for f in files:
        mesh = pv.read(f)
        basename = os.path.basename(f)
        basename = os.path.splitext(basename)[0]
        output_file = os.path.join(outdir, f"conv_{basename}.obj")
        print(f"Converting file: {basename}")

        legend_entries = []
        legend_entries.append(['Liver converted', 'w'])
        plotter = pv.Plotter()
        _ = plotter.add_mesh(mesh)
        _ = plotter.add_legend(legend_entries)
        _ = plotter.export_obj(output_file)
        ret += 1

    print(f"Successfully converted {ret} out of {len(files)} files.")


def run(args):
    convertFiles(args.indir, args.outdir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="VTK to OBJ converter")
    parser.add_argument('indir', help="Path to input directory.")
    parser.add_argument('outdir',help="Path to output directory.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    ret = args.func(args)
