from pytube import YouTube
import os
import subprocess
import PySimpleGUI as sg
import logging

myDirectory = os.getcwd()
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename= "YTapp.log", encoding='utf-8', level=logging.DEBUG)
logging.debug("Beggining of script")
def highRes(url, directory):
    yt = YouTube(url)
    yt.streams.filter(res="1440p",mime_type="video/mp4").first().download(directory + "\\videos")
def midRes(url, directory):
    yt = YouTube(url)
    yt.streams.filter(res="1080p",mime_type="video/mp4").first().download(directory + "\\videos")
def lowRes(url, directory):
    yt = YouTube(url)
    yt.streams.filter(res="720p",mime_type="video/mp4").first().download(directory + "\\videos")
def audio (url, directory):
    yt = YouTube(url)
    yt.streams.filter(only_audio=True, mime_type="audio/webm").first().download(directory + "\\videos")
def merge (video, directory):
    orgAudio = myDirectory + "\\videos\\" + video + ".webm"
    orgVideo = myDirectory + "\\videos\\" + video + ".mp4"
    cmd = "ffmpeg -y -i " + orgAudio + " -r 30 -i " + orgVideo + "  -filter:a aresample=async=1 -c:a flac -c:v copy " + directory + "\\videos\\output\\" + video + ".mkv"
    subprocess.call(cmd, shell=True)
    os.remove(orgAudio)
    os.remove(orgVideo)
def fixNameVid(title):
    fixTitle = title.replace(":", "")
    fixTitle = fixTitle.replace("|", "")
    fixTitle = fixTitle.replace("?", "")
    fixTitle = fixTitle.replace(".", "")
    return fixTitle
def renameVid(directory, oldTitle, newTitle):
    default = directory + "\\videos\\" + oldTitle
    os.rename(default + ".mp4", directory + "\\videos\\" + newTitle + ".mp4")
    os.rename(default + ".webm", directory + "\\videos\\" + newTitle + ".webm")
def renameAudio(directory, oldTitle, newTitle):
    default = directory + "\\videos\\" + oldTitle
    os.rename(default + ".webm", directory + "\\videos\\" + newTitle + ".webm")

sg.theme("Dark2")
layout = [
    [sg.Text("URL:"),sg.Input(key = "-INPUT-"), sg.Button("Add", key = "-ADD-")],
    [sg.Text("Title list:")],
    [sg.Listbox(values=[], select_mode='extended', key='-LIST-', size=(55, 6), background_color="#363636", text_color="White", enable_events= True)],
    [sg.Frame('1440p',[[sg.Button('Download', key = '-1440-'),sg.Text('',key = '-1440p-'),sg.Text('',key = '-BESTSIZE-')]]),
    sg.Frame('1080p',[[sg.Button('Download', key = '-1080-'),sg.Text('',key = '-1080p-'),sg.Text('',key = '-MIDSIZE-')]]),
    sg.Frame('720p',[[sg.Button('Download', key = '-720-'),sg.Text('',key = '-720p-'),sg.Text('',key = '-WORSTSIZE-')]]) ],
    [sg.Frame('Audio only',[[sg.Button('Download', key = '-AUDIO-'),sg.Text('',key = '-AUDIOSIZE-'),sg.Text('',key = '-ASIZE-')]]) ],
    [sg.VPush()],
]
window = sg.Window("myYTdownloader", layout ,icon= myDirectory + "\\logo.ico")

urlList = []
titleList = []
videos = []
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "-ADD-":
        addUrl = values["-INPUT-"]
        urlList.append(addUrl)
        yt = YouTube(addUrl)
        titleList.append(yt.title)
        window["-LIST-"].update(titleList)
    if event == "-LIST-" and len(values['-LIST-']):
        hodnota = (values['-LIST-'][0])
        position = titleList.index(hodnota)
        urlList.pop(position)
        titleList.remove(hodnota)
        window["-LIST-"].update(titleList)
        print(titleList)
        print(urlList)
    if event == "-1440-":
        for url in urlList:
            title = YouTube(url).title
            print("downloading video for " + title  + "at 1440p")
            highRes(url, myDirectory)
            print("download finished")
            print("downloading audio for " + title)
            audio(url, myDirectory)
            print("download finished")
            fixTitle = fixNameVid(title)
            name = fixTitle.replace(" ", "")
            videos.append(name)
            renameVid(myDirectory, fixTitle, name)
        for video in videos:
            merge (video, myDirectory)
    if event == "-1080-":
        for url in urlList:
            title = YouTube(url).title
            print("downloading video for " + title + "at 1080p")
            midRes(url, myDirectory)
            print("download finished")
            print("downloading audio for " + title)
            audio(url, myDirectory)
            print("download finished")
            fixTitle = fixNameVid(title)
            name = fixTitle.replace(" ", "")
            videos.append(name)
            renameVid(myDirectory, fixTitle, name)
        for video in videos:
            merge (video, myDirectory)
    if event == "-720-":
        for url in urlList:
            title = YouTube(url).title
            print("downloading video for " + title  + "at 720p")
            lowRes(url, myDirectory)
            print("download finished")
            print("downloading audio for " + title)
            audio(url, myDirectory)
            print("download finished")
            fixTitle = fixNameVid(title)
            name = fixTitle.replace(" ", "")
            videos.append(name)
            renameVid(myDirectory, fixTitle, name)
        for video in videos:
            merge (video, myDirectory)
    if event == "-AUDIO-":
        for url in urlList:
            title = YouTube(url).title
            print("downloading audio for " + title)
            audio(url, myDirectory)
            fixTitle = yt.title.replace(":", "")
            name = fixTitle.replace(" ", "")
            default = myDirectory + "\\" + fixTitle
            renameAudio(myDirectory, fixTitle, name)
            print("download finished")
window.close()