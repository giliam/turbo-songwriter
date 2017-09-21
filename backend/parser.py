from songwriter.parser import Parser
parser = Parser("../data/file/word/document.xml")
parser.parse()
parser.save_songs()
parser.compile()