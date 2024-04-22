import os


def analyze_content(content):
    # Dummy function for analysis
    # Replace or extend this function with actual analysis logic
    return f"Analysis results: {len(content)} characters"


def process_files():
    base_dir = "SANSTOP25"
    results_dir = "results"

    # Ensure the results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # Iterate over each subdirectory in the base directory
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)

        # Check if it's a directory
        if os.path.isdir(subdir_path):
            # Prepare a results subfolder path
            result_subdir = os.path.join(results_dir, subdir)
            os.makedirs(result_subdir, exist_ok=True)

            # Process each file in the subdirectory
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)

                # Open and read the file content
                with open(file_path, "r") as f:
                    content = f.read()

                # Perform analysis
                result = analyze_content(content)

                # Write the analysis results to a new file in the results subdirectory
                result_file_path = os.path.join(result_subdir, file + ".analysis.txt")
                with open(result_file_path, "w") as result_file:
                    result_file.write(result)


if __name__ == "__main__":
    process_files()
