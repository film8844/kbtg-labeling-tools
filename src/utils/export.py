def write_to_yolo_format(data, output_file):
    with open(output_file, 'w') as f:
        for item in data:
            x_center = item['x']
            y_center = item['y']
            width = item['width']
            height = item['height']
            class_id = item['classname']

            # Write to file in YOLO format
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

def create_classes_txt(data,output_file):
    with open(output_file, 'w') as f:
        for item in data:
            f.write(f"{item}\n")
