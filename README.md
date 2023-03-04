# Rook
*Bash*
---

I named it rook, because I was just getting into chess at that time, nothing special about the name.

MD5 is a 128-bit cryptographic hash and is used properly it can be used to verify the authenticity and integrity of a file.

Software distributors give you the checksum of the file you are downloading, this **md5** or **sha256 checksum** will help you make sure, that the file was **not tampered** with by a third party or a malicious user.

If you find, that the checksum of the downloaded file is different from the one that is provided by the distributor, it is possible that the downloaded file was **corrupted or there was a comprimise in the integrity of the file.**

## What is Rook?

Rook is a tool I developed using bash scripting. It calculates the md5 hashes of all the 
files in a given directory recursively and writes it into a *.rk* file in the format.

The Directories to be scanned can be provided line by line in the scanme file. *scanner.sh* takes scanme as an input.

``dd-mm-yy-hh-mm-ss.rk``

We can compare two log file using the command

``diff <file1.rk> <file2.rk> -e``
``diff <file1.rk> <file2.rk> -n``

If there is one of the following changes the diff command will show you:

* Change in a file's contents
* Moved into a different directory
* A file was deleted
* A file was created
* Creation of a duplicate file

## DEMO

**Before Changes**
![Before Changes](https://github.com/saai-sudarsanan-d/Rook-DirectoryIntegrityCheck/blob/main/before-changes.png)

**Changing**
![Changing](https://github.com/saai-sudarsanan-d/Rook-DirectoryIntegrityCheck/blob/main/malicious-change.png)

**After Changes**
![After Changes](https://github.com/saai-sudarsanan-d/Rook-DirectoryIntegrityCheck/blob/main/after-changes.png)

**diff Command**
![diff](https://github.com/saai-sudarsanan-d/Rook-DirectoryIntegrityCheck/blob/main/diff.png)

## Drawbacks

* Doesn't detect if only the file's meta-data was changed
* Doesn't detect if file permissions was changed* (Serious Issue)

In Linux File Permissions are stored in Inodes  along with the following details : 

* Creation, read, and write timestamps
* Location of the data
* User and group IDs associated with the file
* File size

A Simple solution will be to compress each file into a *tar archive* which will preserve the permissions of the file.

### Example

![Example use of tar](https://github.com/saai-sudarsanan-d/Rook-DirectoryIntegrityCheck/blob/main/permission-change.png)

This way we can check for changes in file permissions also.

Thank You :)
