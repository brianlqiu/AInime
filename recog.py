import os, argparse, glob, sys, decimal

def analyze_recognized(char):
    num_orig = len(os.listdir(f'raw_images/validation/{char}')) + len(os.listdir(f'raw_images/training/{char}'))
    print(f'Number of raw images for {char}: {num_orig}')
    num_missing = 0
    missing_list = []
    for i in range(num_orig):
        if len(glob.glob(f'cropped_images/{char}/{char}{i}*')) == 0:
            print(f'Image {i} was unrecognized')
            missing_list.append(i)
            num_missing += 1

    print(f'Number of recognized images for {char}: {num_orig - num_missing}')
    print(f'Number of unrecognized images for {char}: {num_missing}')

    percent = decimal.Decimal(100.0 * ((num_orig - num_missing) / num_orig))

    with open('recog.log', 'a') as fp:
        fp.write(f'{char}\n')
        fp.write(f'Original:            {num_orig}\n')
        fp.write(f'Recognized:          {num_orig - num_missing}\n')
        fp.write(f'Percent recognized:  {round(percent, 1)}%\n')
        fp.write('Unrecognized values: ' + '[' + ','.join(str(item) for item in missing_list) + ']\n\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Walk directory to check number of recognized files')
    parser.add_argument('character', action='store')
    args = parser.parse_args(sys.argv[1:])

    analyze_recognized(args.character)
            