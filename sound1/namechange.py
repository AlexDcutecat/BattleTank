import os

def changename():
    file_list=([filename for filename in os.listdir(os.getcwd())])

    print(file_list)
    

if __name__ == '__main__':
    changename()
