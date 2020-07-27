__author__ = 'Brian M Anderson'
# Created on 7/24/2020

import os
from Dicom_RT_and_Images_to_Mask.Image_Array_And_Mask_From_Dicom_RT import Dicom_to_Imagestack


def convert_rts(base_path):
    for path, directories, files in os.walk(base_path):  # Look through all folders
        files = [i for i in files if i.endswith('.dcm')]  # Stop if we have something with dicom
        if files and len(files) > 5 and 'New_RT' not in directories:  # Only go forward if we have at least 5 images
            base_reader = Dicom_to_Imagestack(get_images_mask=False)  # Make a base reader to identify the contour names
            base_reader.down_folder(path)
            Contour_Names = base_reader.rois_in_case  # Keep the same nomenclature for naming
            if not Contour_Names:
                print('No contours found at {}'.format(path))
                continue
            reader = Dicom_to_Imagestack(get_images_mask=True,
                                         Contour_Names=Contour_Names,
                                         arg_max=False)  # Now, create a new reader to create a mask of the contours
            reader.Make_Contour_From_directory(path)  # Create the images and mask from the path
            reader.use_template()  # Shift over to our template for re-writing them
            reader.with_annotations(reader.mask, output_dir=os.path.join(path,'New_RT'),
                                    ROI_Names=Contour_Names)  # Write the new RT structure out


if __name__ == '__main__':
    convert_rts(base_path=r'K:\Morfeus\YHe\Brian\correct')
