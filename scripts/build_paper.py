"""Run the included standard-profile manuscript exporter."""
import argparse, pathlib, subprocess

root=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir',type=pathlib.Path,default=root/'build/paper')
args=parser.parse_args()
subprocess.run(['bash',str(root/'scripts/export_markdown.sh'),'--profile','standard',
                '--keep-work','--output-dir',str(args.output_dir.resolve()),
                '--output-stem','manuscript',str(root/'paper/manuscript.md')],check=True)
