from optparse import OptionParser
import generate_metadata_csv
import download_metadata
import parse_metadata
import threading
import itertools
import time
import sys
import os

# Set default string processing to Unicode-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# global variables
done = False

# loading animation


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)


def main(name, start, end, time, overwrite):
    directory = "%s_%s_%s" % (name, start, end)
    if overwrite is True or directory not in os.listdir(os.getcwd()):
        if directory not in os.listdir(os.getcwd()):
            os.mkdir(directory)
        for i in os.listdir(directory):
            os.system("rm %s" % directory + "/" + i)
        os.chdir(directory)
        start_date = start.replace("-", "/")
        end_date = end.replace("-", "/")
        # Build the query term
        query = "(%s[Organism]) AND (\"%s\"[Publication Date] : \"%s\"[Publication \
              Date])" % (name, start_date, end_date)
        # Run the program
        download_metadata.main(query, time)
        print "\nFinished downloading metadata\nParsing XML files"

    # Get xml_files inside of path
    xml_files = os.listdir(directory)
    data = []
    # Parse all of the xml data together
    for i in xml_files:
        data.append(parse_metadata.main(directory + "/" + i))
    print "Finished parsing XML files\nWriting to CSV"

    # Write to csv based on xml files
    generate_metadata_csv.main(data, directory)

    # print "Cleaning up\n"
    # for i in xml_files:
    #     os.system("rm %s" % path + "/" + i)
    # os.system("rmdir %s" % path)

if __name__ == "__main__":
    os.chdir(os.getcwd())
    # Process the command line input using optparse
    usage = "usage: %prog options"
    parser = OptionParser(usage=usage)
    parser.add_option("-n", "--name", help="query organsim name", dest="name")
    parser.add_option("-s", "--start", help="query start date (YYYY-MM-DD)",
                      dest="start")
    parser.add_option("-e", "--end", help="query end date (YYYY-MM-DD)",
                      dest="end")
    parser.add_option("-t", "--time", help="increase to set longer times\
                      between accession, default 0.1 sec", dest="time",
                      default=0.1)
    parser.add_option("-o", "--overwrite", help="set to True/T to overwrite\
                      existing xml files", default=False)
    (options, args) = parser.parse_args()

    # Raise optparse errors as necessary
    if options.name is None:
        parser.error("Please provide a name to query")
    if options.start is None or options.end is None:
        parser.error("Please provide a start and end date for which to query")
    # Create loading animation
    t = threading.Thread(target=animate)
    t.start()

    main(options.name, options.start, options.end, float(options.time),
         bool(options.overwrite))

    done = True
