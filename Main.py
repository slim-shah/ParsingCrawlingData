from ParseCrawlingDump import ParseDump

def main():
    P = ParseDump()
    P.Read_File("D:\Cranfield\dump")
    P.Compute_Page_Rank()
    P.Save_Data()

main()