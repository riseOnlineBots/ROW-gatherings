import os


# if key == ord('z'):
#     cv2.destroyAllWindows()
#     break
# elif key == ord('f'):
#     cv2.imwrite('copperMines/positive/{}.jpg'.format(loop_time), screenshot)
#     print('Screenshot taken.')
# elif key == ord('d'):
#     cv2.imwrite('copperMines/negative/{}.jpg'.format(loop_time), screenshot)
#     print('Screenshot taken.')

# Call these functions in terminal to create files.
# python
# from cascadeutils import generate_negative_description_file, generate_positive_description_file
# generate_negative_description_file()

def generate_negative_description_file():
    with open('copperMines/neg.txt', 'w') as f:
        for filename in os.listdir('copperMines/negative'):
            f.write('copperMines/negative/' + filename + '\n')


def generate_positive_description_file():
    with open('copperMines/pos.txt', 'w') as f:
        for filename in os.listdir('copperMines/positive'):
            f.write('copperMines/positive/' + filename + '\n')

# https://nav.dl.sourceforge.net/project/opencvlibrary/3.4.11/opencv-3.4.11-vc14_vc15.exe
# C:\Users\undefined\Downloads\opencv\build\x64\vc14\bin\opencv_annotation.exe --annotations=pos.txt --images=copperMines\positive\
# * mark rectangles with the left mouse button,
# * press 'c' to accept a selection,
# * press 'd' to delete the latest selection,
# * press 'n' to proceed with next image,
# * press 'esc' to stop.

# Then
# C:\Users\undefined\Downloads\opencv\build\x64\vc14\bin\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec
# Play with w and h.
# Go to pos.txt, and replace \ to /.

# Then
#  C:\Users\undefined\Downloads\opencv\build\x64\vc14\bin\opencv_traincascade.exe -d
# ata cascade/ -vec pos.vec -bg .\copperMines\neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -w 26 -h 26 -maxFalseAlarmRate 0.3 -minRate 1 -numPos 24 -numNeg 110 -numStages 10
# Play with numbers. numPos should be less than the rectangles we drew. numNeg could be higher.
# N: Layer number. #HR: Hit rate #FA: False alarm
# Note: NEG count : acceptanceRatio    7 : 0.000922145 - if 4 digits show up, that means we over-trained the AI.
