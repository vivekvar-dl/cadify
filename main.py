import os
import sys
from dotenv import load_dotenv
from cad3dify import generate_step_from_2d_cad_image


def main():
    load_dotenv()
    
    # Use command line arguments if provided, otherwise use defaults
    folder_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    
    if len(sys.argv) > 1:
        image_filepath = sys.argv[1]
        output_filepath = sys.argv[2] if len(sys.argv) > 2 else os.path.join(folder_path, 'output.step')
    else:
        # Default files
        image_filepath = os.path.join(folder_path, 'sample_data/a-23.jpg')
        output_filepath = os.path.join(folder_path, 'sample_data/output.step')
    
    print(f"Processing image: {image_filepath}")
    print(f"Output will be saved to: {output_filepath}")
    
    generate_step_from_2d_cad_image(image_filepath, output_filepath)


if __name__ == "__main__":
    main()
