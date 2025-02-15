import argparse
from editor import edit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates automatic subtitles for a given video.")
    parser.add_argument('-f','--input-file',  required=True, help="Input video file")
    parser.add_argument('-o','--output-file', required=True, help="Output video file")

    parser.epilog = """Example usage:
    python auto_sub.py -f input.mp4 -o output.mp4
    """
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    # Call the edit function from editor.py
    edit(input_file, output_file)
