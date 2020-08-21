import os, argparse, glob, sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Walk directory to check number of recognized files')
    parser.add_argument('character', action='store')
    parser.add_argument('recog_type', action='store')
    args = parser.parse_args(sys.argv[1:])

    num_orig = len(os.listdir(f'images/{args.character}'))
    print(f'Number of raw images for {args.character}: {num_orig}')

    num_missing = 0
    missing_list = []
    f'{args.recog_type}/{args.character}'
    for i in range(num_orig):
        if len(glob.glob(f'{args.recog_type}/{args.character}/{args.character}{i}*')) == 0:
            print(f'Image {i} was unrecognized')
            missing_list.append(i)
            num_missing += 1

    print(f'Number of recognized images for {args.character}: {num_orig - num_missing}')
    print(f'Number of unrecognized images for {args.character}: {num_missing}')

    with open('test.log', 'a') as fp:
        fp.write(f'{args.recog_type}\n')
        fp.write(f'Original:        {num_orig}\n')
        fp.write(f'Recognized:      {num_orig - num_missing}\n')
        fp.write(f'Unrecognized:    {num_missing}\n')
        fp.write('[' + ','.join(str(item) for item in missing_list) + ']\n\n')
            