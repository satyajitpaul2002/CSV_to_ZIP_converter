import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the CSV file
file_path = r"C:\Users\SATYAJIT\Downloads\Data\freshers (1).csv"   # change with your file name
df = pd.read_csv(file_path)

# Select only required columns
df = df[[
    "First Name",
    "Last Name",
    "Email",
    "Mobile No",
    "Highest qualification",
    "Work Experience",
    "Location",
    "Sub-Location",
    "State"
]]

# Create output folder
output_dir = "split_images_selected"
os.makedirs(output_dir, exist_ok=True)

# Loop through dataframe in chunks of 5
for i in range(0, len(df), 5):
    chunk = df.iloc[i:i+5]

    # Make a bigger figure to avoid overlapping
    fig, ax = plt.subplots(figsize=(20, 2 + 0.6*len(chunk)))
    ax.axis('off')

    # Render chunk as table
    table = ax.table(cellText=chunk.values,
                     colLabels=chunk.columns,
                     cellLoc='center',
                     loc='center')

    # Adjust font and scaling
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    # Save as JPG
    file_name = f"freshers_part_{i//5 + 1}.jpg"
    plt.savefig(os.path.join(output_dir, file_name), bbox_inches='tight', dpi=200)
    plt.close()

print("Selected columns have been saved as JPG images inside 'split_images_selected' folder.")
