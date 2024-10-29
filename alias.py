import logging

class Alias:
    def __init__(self, alias: str = "", english: str ="", polish: str = ""):
        self.alias = alias.strip()
        self.english = english.strip()
        self.polish = polish.strip()

    def print_alias(self):
        return f".{self.alias} {self.english}\n..{self.alias} {self.polish}\n.{self.alias}pl {self.polish}"

    def __str__(self):
        return f".{self.alias} {self.english} / {self.polish}"


class AliasFile:

    def read_file(self, file_path: str):
        logging.debug("Reading file " + file_path  )
        with open(file_path, "r") as file:
            for line in file:
                #print(line)
                # Skip comment lines
                if line.startswith(';'):
                    logging.debug("Skipping comment line: " + line)
                    continue
                # Skip empty lines
                if len(line.strip()) == 0:
                    logging.debug("Skipping empty line.")
                    continue
                entry = Alias()
                line_is_polish = False
                # skip too short lines
                if len(line.split(" ",1)) < 2:
                    logging.warning("Skipping too short line: " + line)
                    continue
                [alias, contents] = line.split(" ", 1)
                contents = contents.strip()
                if alias.startswith(".."):
                    line_is_polish = True
                alias = alias.replace(".", "")
                if alias.endswith("pl"):
                    line_is_polish = True
                    alias = alias[:-2]
                entry.alias = alias
                if self.aliases.__contains__(alias):
                    entry = self.aliases[alias]
                if line_is_polish:
                    entry.polish = contents
                else:
                    entry.english = contents
                self.aliases[alias] = entry

    def __init__(self):
        self.aliases = dict()

    def print_aliases(self):
        for alias, entry in self.aliases.items():
            print(entry.print_alias())

    def save_to_file(self, file):
        with open(file, "w") as file:
            for alias, entry in self.aliases.items():
                file.write(entry.print_alias() + "\n")