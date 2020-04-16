import csv

def mergeFiles():
    in_1_name = "../files/2016_Jan_New.csv"
    in_2_name = "../files/kmean4_data.csv"
    out_name = "../files/merged_jan.csv"

    with open(in_1_name) as in_1, open(in_2_name) as in_2, open(out_name, 'w') as out:
        reader1 = csv.reader(in_1, delimiter=";")
        reader2 = csv.reader(in_2, delimiter=";")
        writer = csv.writer(out, delimiter=";")
        for row1, row2 in zip(reader1, reader2):
            if row1[0] and row2[0]:
                writer.writerow([row1[0], row2[0]])

def correctDelimiter():
    text = open("../files/merged_jan.csv", "r")
    text = ''.join([i for i in text]) \
        .replace(";", ",")
    x = open("../files/merged_jan.csv","w")
    x.writelines(text)
    x.close()

def main():
    mergeFiles()
    correctDelimiter()

if __name__ == "__main__":
    main()

