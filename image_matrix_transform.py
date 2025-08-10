import cv2
import numpy as np
import os

def transform_image_autofit(input_path: str, output_path: str, T: np.ndarray):
    image = cv2.imread(input_path)
    if image is None:
        print(f"Error: Can't read from '{input_path}'")
        return


    (h, w) = image.shape[:2]

    corners = np.array([
        [0, 0, 1],
        [w - 1, 0, 1],
        [0, h - 1, 1],
        [w - 1, h - 1, 1]
    ]).T 


    transformed_corners = T @ corners
    x_coords = transformed_corners[0, :]
    y_coords = transformed_corners[1, :] 
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    new_w = int(np.ceil(x_max - x_min))
    new_h = int(np.ceil(y_max - y_min))
    M = T[0:2, :].copy() 
    M[0, 2] -= x_min 
    M[1, 2] -= y_min
    transformed_image = cv2.warpAffine(image, M, (new_w, new_h))
    
    try:
        cv2.imwrite(output_path, transformed_image)
        print(f"\nSaved to:'{output_path}'")
        print(f"Init Resolution: {w}x{h}, New Resolution: {new_w}x{new_h}")
    except Exception as e:
        print(f"Can't save to path:'{output_path}': {e}")
def get_user_input():
    while True:
        input_path = input("Source File Path: ")
        if os.path.exists(input_path):
            break
        else:
            print("Error:File Doesn't Exist")

    output_path = input("Save to path: ")
    print("[ a11, a12, tx ]\n[ a21, a22, ty ]\n[  0,   0,   1 ]")
    print("-" * 20)

    def get_float_input(prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Value Error")
    
    a11 = get_float_input("a11: ")
    a12 = get_float_input("a12: ")
    tx = get_float_input("tx: ")
    a21 = get_float_input("a2: ")
    a22 = get_float_input("a22: ")
    ty = get_float_input("ty: ")

    T = np.array([[a11, a12, tx], [a21, a22, ty], [0.0, 0.0, 1.0]])
    
    print(T)
    return input_path, output_path, T

if __name__ == '__main__':

    input_file, output_file, T_matrix = get_user_input()
    

    while True:
        mode = input("Resolution Adjustment？ (y/n): ").lower()
        if mode in ['y', 'n']:
            break
        else:
            print("PLEASE KEY 'y' or 'n'")

    if mode == 'y':
        transform_image_autofit(input_file, output_file, T_matrix)
    else:
        print("WARNING:IMAGE WILL BE IMCOMPLETE")
        image = cv2.imread(input_file)
        h, w = image.shape[:2]
        M = T_matrix[0:2, :]
        transformed_image = cv2.warpAffine(image, M, (w, h))
        cv2.imwrite(output_file, transformed_image)
        print(f"\nSaved To:'{output_file}'")