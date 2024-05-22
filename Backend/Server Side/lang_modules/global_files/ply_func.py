import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

count = 0
key = b'0123456789abcdef0123456789abcdef'

def encrypt_data(key, data):
    chunksize = 64 * 1024
    output_data = b""
    filesize = str(len(data)).zfill(16).encode('utf-8')
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    output_data += filesize
    output_data += IV

    padded_data = pad(data, AES.block_size)
    for i in range(0, len(padded_data), chunksize):
        chunk = padded_data[i:i + chunksize]
        output_data += encryptor.encrypt(chunk)

    return output_data


def decrypt_data(key, encrypted_data):
    chunksize = 64 * 1024
    output_data = b""
    if len(encrypted_data) < 16:
        return b""

    offset = 16
    try:
        filesize = int.from_bytes(encrypted_data[:offset], byteorder='big')
    except ValueError:
        return b""

    iv = encrypted_data[offset:offset + 16]
    encrypted_data = encrypted_data[offset + 16:]

    decryptor = AES.new(key, AES.MODE_CBC, iv)

    while encrypted_data:
        chunk = encrypted_data[:chunksize]
        encrypted_data = encrypted_data[chunksize:]
        decrypted_chunk = decryptor.decrypt(chunk)
        output_data += unpad(decrypted_chunk, AES.block_size)

    return output_data[:filesize]

def count_ply(path):
    global count
    for dir_path in os.listdir(path):
        if os.path.isfile(os.path.join(path,dir_path)):
            count += 1
    return count

def create_ply(filename,extension,dir):
    filepath = os.path.join(dir, filename + extension)
    with open(filepath,"w") as f:
        f.write("")

def del_ply(dir, filename, extension):
    filepath = os.path.join(dir, filename + extension)
    if os.path.exists(filepath):
        os.remove(filepath)
        print("Playlist '{}' deleted successfully.".format(filename))
    else:
        print("Playlist '{}' does not exist.".format(filename))

def add_song_ply(filename, extension, dir, data):
    global key
    filepath = os.path.join(dir, filename + extension)

    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()
        existing_data = decrypt_data(key, encrypted_data)
        new_data = existing_data + b'\n' + data.encode()
    else:
        new_data = data.encode()

    encrypted_data = encrypt_data(key, new_data)
    with open(filepath, 'wb') as f:
        f.write(encrypted_data)

    print("SUCCESSFULLY ENCRYPTED AND WRITTEN")

def get_song_data():
    pass

def remove_song_ply(filename, extension, dir, search_term):
    global key
    filepath = os.path.join(dir, filename + extension)

    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            encrypted_data = f.read()
        existing_data = decrypt_data(key, encrypted_data)
        lines = existing_data.decode().split('\n')
        new_lines = [line for line in lines if search_term.lower() not in line.lower()]
        new_data = b'\n'.join(line.encode() for line in new_lines)

        encrypted_data = encrypt_data(key, new_data)
        with open(filepath, 'wb') as f:
            f.write(encrypted_data)

        print(f"Lines containing '{search_term}' removed successfully.")
    else:
        print("FILE DOES NOT EXIST")

def find_no_of_songs():
    pass

def most_played():
    pass

def least_played():
    pass

def total_ply_hours():
    pass

#------------DEBUGGER-------------#

if __name__ == "__main__":
    print("Enter the command")
    ply_path = r'D:/3DavatarAssistant/Backend/Server Side/Playlists/'
    extension = ".xtx"
    while True: 
        uinput = str(input()) 
        # splitting the uinput in 2 strings and access the first string 
        if uinput == "count": 
            print("TOTAL NO OF FILES : ",count_ply(ply_path))
  
        elif uinput == "create": 
            filename = input("Enter the playlist name : ")
            create_ply(filename,extension,ply_path)
            print("PLAYLIST CREATED SUCCESSFULLY")

        elif uinput == "addsong":
            filename = input("Enter the playlist name : ")
            filepath = os.path.join(ply_path, filename + extension)

            if os.path.exists(filepath):
                data = input("Enter the data to be added: ")
                add_song_ply(filename, extension, ply_path, data)
            else:
                print("FILE DOES NOT EXIST")
        
        elif uinput == 'delete': 
            Name = str(input("enter name of playlist:")) 
            del_ply(ply_path,Name,extension)

        elif uinput == 'decrypt':
            filename = input("Enter the playlist name: ")
            filepath = os.path.join(ply_path, filename + extension)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = decrypt_data(key, encrypted_data)
                if decrypted_data:
                    lines = decrypted_data.decode().split('\n')
                    for line in lines:
                        if line.strip():  # Skip empty lines
                            print(line)
                else:
                    print("FILE IS EMPTY OR CORRUPTED")
            else:
                print("FILE DOES NOT EXIST")

        elif uinput == 'delsong':
            filename = input("Enter the playlist name: ")
            search_term = input("Enter the song Name : ")
            remove_song_ply(filename, extension, ply_path, search_term)
        '''
        elif uinput == "pt": 
            pName = uinput.split(" ", 1)[1] 
            streamPlaylist(pName) 
  
        elif uinput.split(" ", 1)[0] == "rem": 
            name = str(input("Enter name to remove playlist") 
            removePlaylist(name) 
  
        elif uinput == "stop": 
            stop() 
  
        else: 
            print("invalid command") 
        '''