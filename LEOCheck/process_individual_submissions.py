import zipfile
import os
import xml.etree.ElementTree as ET

# Note: you need to run the script TWICE
# First time to exact the zipped file submission in each student folder
# Second time to go through the exacted files to analyse the content

# Sample directory structure
# - 6_individual_ file submission
# -- C236-2D-HB01-A
# --- 170000002_Henry Lee
# --- 170000003_Henry Tan
# -- C236-4D-HB01-A
# --- 170000004_Mary Lee
# --- 170000006_Mary Tan

lesson = "P13"  # lesson number
path = "D:\Check\Web App Development in .NET\\" + lesson # directory path of the extracted students submission
days = ["C236-1D-HB04-A"] # class names, representing the two folders inside the path above
original_files = ["MovieController.cs","ChartController.cs","Movie.cs","ListMovies.cshtml","EditMovie.cshtml","Summary.cshtml"] # required code files

# [missingDoc, editingShort, missingCode, missingComment, extraFile]
def search_files(path, stdId, name, status, code_files):
    for item in os.listdir(path):
        one_path = os.path.join(path, item)
        if os.path.isdir(one_path):
            [status, code_files] = search_files(one_path, stdId, name, status, code_files)
        elif item.endswith(".zip"):
            print("Error! Zip file:", item)
        elif item.endswith(".html") or item.endswith(".cshtml"):
            status[2] = False
            for one_file in code_files:
                if item.lower() == one_file.lower():
                    # print("to remove: ",one_file)
                    code_files.remove(one_file)
                    break
            # if item in code_files:
            #     code_files.remove(item)

            f = open(one_path, "r", encoding='UTF-8')
            text = f.read()
            if ("<!--" not in text or "-->" not in text) and ("//" not in text):
                if not status[3]:
                    print("Error! No comment:", item)
                status[3] = True
            else:
                # id_name = text.split("<!--")[1].split("-->")[0]
                # print(id_name)
                if stdId not in text:
                    # if not status[3]:
                    print("ERROR: No comment or Copied from others? ", item)
                    status[3] = True
        elif item.endswith(".cs"):
            for one_file in code_files:
                if item.lower() == one_file.lower():
                    # print("to remove: ",one_file)
                    code_files.remove(one_file)
                    break
            f = open(one_path, "r", encoding='UTF-8')
            text = f.read()
            if "//" not in text:
                if not status[3]:
                    print("Error! No comment:", item)
                status[3] = True
            elif stdId not in text:
                # if not status[3]:
                print("ERROR: No comment or Copied from others? ", item, stdId)
                status[3] = True
        elif item.endswith(".docx") and not item.startswith("~$"):
            status[0] = False
            unzipped_file = zipfile.ZipFile(one_path, "r")
            a_file = unzipped_file.read("docProps/app.xml")
            root = ET.fromstring(a_file)
            editingTime = int(root[1].text)
            if editingTime < 5:
                # print("Error! Editing time too short!", item)
                status[1] = True
            core_file = unzipped_file.read("docProps/core.xml")
            root = ET.fromstring(core_file)
            last_edited = root[5].text
            if name[:14] != last_edited[:14]:
                print("Error!!! name does not match! Last edited by",last_edited)
        elif item.endswith(".jpg") or item.endswith(".png"):
            print("Don't need to upload image file next time")
        elif item.endswith(".pdf"):
            print("Certificate file present!")
        else:
            if not status[4]:
                print("Error! Unknown file type: ",item)
            status[4] = True
    return [status, code_files]


for one_class in os.listdir(path):
    print(one_class)
    if one_class not in days:
        print("skip!")
        continue
    idList = []
    nameList = []
    one_class_dir = os.path.join(path, one_class)
    for one_std in os.listdir(one_class_dir):
        # print(one_std)

        result = one_std.split("_")
        stdId = result[0]
        name = result[1]
        idList.append(stdId)
        nameList.append(name)
        print(stdId, name)
        one_std_dir = os.path.join(one_class_dir, one_std)
        zip_found = False
        for one_file in os.listdir(one_std_dir):
            file_path = os.path.join(one_std_dir, one_file)
            if os.path.isdir(file_path): # zip file extracted already
                status = [True, False, False, False, False]
                code_files = original_files.copy()
                [status, code_files] = search_files(file_path, stdId, name, status, code_files)
                [missingDoc, editingShort, missingCode, missingComment, extraFile] = status
                print("[missingDoc, editingShort, missingCode, missingComment, extraFile]")
                print(status)
                penalty = 0
                if editingShort:
                    print("Editing time is too short: SDL set to 3 or 4")
                print("Copy/paste comment below:")
                if editingShort:
                    print("Worksheet: Editing time is too short.")
                # if missingCode:
                #     print("Missing code.")
                if len(code_files) > 0:
                    print("Missing code: " + str(code_files))
                if missingComment:
                    print("Code: Missing comment line with your student id and name.")
                    # penalty+=10
                if extraFile:
                    print("Don't include other code/project files in the submission.")
                    # penalty += 10

                if missingDoc:
                    print("Missing worksheet document.")
                if penalty >0:
                    print("penalty:")
                    print(penalty)
            elif one_file.endswith(".zip"):
                zip_found = True
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    target_dir = os.path.join(one_std_dir, one_file[:-4])
                    if not os.path.exists(target_dir):
                        zip_ref.extractall(target_dir)
                        # print("one zip file extracted")
                    # else:
                    #     print("Warning: Target directory already exist, file extracted already?")

            elif one_file.endswith(".rar") or one_file.endswith(".7z"):
                print("Please upload using zip file instead of rar/7z")
                print("Penalty (together with upload project file): 10")
            elif one_file.endswith(".docx"):
                print("Please zip the worksheet document together with code files. ")
            elif one_file.endswith(".pdf"):
                print("Warning: PDF file not inside zip:",one_file)
            else:
                print("Other file format:", one_file)
        if not zip_found:
            print("ERROR: didnot upload zip file at all")
        print()




