#include<iostream>
#include<fstream>

using namespace std;

// Declaring language constructs
const char delimiters[] = {' ', ';', '(', ')', 
                        ']', '[', '{', '}', '"', '#', ';', ',', '\''
                        , ':'};

const char operators[] = {'+', '-', '*', '^', 
                    '/', '>', '<', '=', '.', '%', '&', '|', '~', ','};

const string binaryOperators[] = {"<<", "++", "--", "+=", "-=", "*=", "/=", ">>", "&&",
                        "||", "!="};

const string keywords[] = {"if", "else", "while", "do", "break", "continue",
        "int", "double", "float", "return", "char", "string", "case", "sizeof", 
            "long", "short", "typedef", "switch", "unsigned", "void", "struct", "goto", "static",
            "class", "for", "continue", "private", "include", "iostream", "using", "namespace", "std", "cout"
            , "endl", "public"};


string symbolTable[1024];
int symbolIndx = 0;

bool isDelimiter(char ch) {
    for(char c: delimiters){
        if(ch == c){
            return true;
        }
    }
    return false;
}

bool isOperator(char ch){
    for(char c: operators){
        if(ch == c){
            return true;
        }
    }
    return false;
}

bool isKeyWord(string str){
    for(string key: keywords){
        if(key == str){
            return true;
        }
    }
    return false;
}

bool isNum(char c){
    int code = (int)c;
    if(!(48 <= code && code <=57)){
        return false;  
    }
    return true;
}

bool isInteger(string str){
    for(char c: str){
        if(!isNum(c)){
          return false;  
        }
    }
    return true;
}


bool isReal(string str){
    bool hasDecimal = false;
    for(char c: str){
        if(c == '.'){
            hasDecimal = true;
            continue;
        }
        if(!isNum(c)){
          return false;  
        }
    }
    return hasDecimal;
}

bool isAlphabet(char c){
    if((97 <= c && c <= 122) || (65 <= c && c <= 90)){
        return true;
    }
    return false;
}

bool isBinaryOperator(char op1, char op2){
    for(string s: binaryOperators){
        if(s[0] == op1 && s[1] == op2){
            return true;
        } 
    }
    return false;
}

void addSymbol(string s){
    symbolTable[symbolIndx++] = s;
}

/*
    Identifier can contain letter, digits and underscores.
    Names must begin only with a letter or an underscore
    Names cannot contain whitespace or special characters
*/
bool isIdentifier(string str){
    if(!isAlphabet(str[0]) && str[0] != '_'){
        return false;
    }
    for(char c: str){
        if(!isAlphabet(c) && !isNum(c) && (c != '_')){
            return false;
        }
    }
    return true;
}

bool checkTable(string str){
    for(int i=0; i<symbolIndx; i++){
        if(str == symbolTable[i]){
            return true;
        }
    }
    return false;
}

void parse(string uri){
    string buff, str;
    ifstream stream(uri);
    bool indentifier = false;
    bool comments = false, multiLineComment = false;
    bool rvalue = false;

    if(!stream.is_open()){
        throw runtime_error("Could not open the file");
        exit(1);
    }



    while(getline(stream, str, ';')){

        indentifier = false;

        for(int i=0; i<str.length(); i++){
           
            // We dont want to show comments, spaces and newline in output hence wer skipping it
            if(i > 0 && str[i] == '/' && str[i-1] == '*'){
                multiLineComment = false;
                continue;
            }

            if(str[i] == ' '|| str[i] == '\n' || str[i] == '\t' || comments == true 
                || multiLineComment == true){
                if(str[i] == '\n')
                    comments = false;
                buff = "";
                continue;
            }


            buff = buff + str[i];

            if((i == (str.length() - 1)) 
                || isDelimiter(str[i+1]) || isOperator(str[i+1])
                || isDelimiter(str[i]) || isOperator(str[i])){

                if(isDelimiter(buff[0])){
                   

                    if(buff[0] == '"'){
                        i++;
                        while(str[i] != '"'){
                            if(str[i] != '\n')
                                cout << str[i];
                            i++;
                            if(i >= str.length()) throw runtime_error("missing \'\"\'");
                        }
                        cout << " is string" << endl;
                        continue;

                    }

                    if(buff[0] == '\''){
                        cout << str[i+1] << " is character" << endl;
                        i+=2;
                        cout << (bool)(str[i] != '\'');
                        if(i < str.length() && str[i] != '\'') throw runtime_error("invalid character declaration");
                        continue;

                    }

                    
                } 
                else if(isOperator(buff[0])){
                     /*
                        In c++ identifier is also valid after ','. Eg: int a, b;
                    */
                    if(indentifier == true && buff[0] == ',') {
                        indentifier =  true; 
                        rvalue = false;
                    }

                    if(isBinaryOperator(buff[0], str[i+1])){
                        cout << buff[0] << str[i+1];
                        i+=1;
                    } 
                    // Ignoring comments
                    else if(buff[0] == '/' && str[i+1] == '/'){
                        comments = true;
                        i++;
                        continue;
                    } else if(buff[0] == '/' && str[i+1] == '*'){
                        multiLineComment = true;
                        i++;
                        continue;
                    }
                    else{
                        cout << buff[0];
                    } 
                    cout << " is operator" << endl;
                    if(buff[0] == '=')
                        rvalue = true;
                }
                else if(isKeyWord(buff)){
                    cout << buff << " is keyword" << endl;
                    indentifier = true;
                }
                else if(isInteger(buff)){
                    cout << buff << " is integer" << endl;
                }
                else if(isReal(buff)){
                    cout << buff << " is real number" << endl;
                }
                else if(isIdentifier(buff)){
                    if(indentifier && !rvalue && !checkTable(buff)){
                        addSymbol(buff);
                    } else {
                        if(checkTable(buff)){
                            indentifier = true;
                        } else{
                            throw runtime_error(buff + " identifier is not declared");
                            buff = "";
                            continue;
                        }
                    }                      
                    cout << buff << " is identifier" << endl;

                }else {
                    throw runtime_error(buff + " is not valid identifier");
                }
                
                buff = "";
            }
        }
    }

}

int main() {
    // Set the file location
    parse("./code.txt");

    // cout << "Symbol Table " << endl;
    // for(int i=0; i<symbolIndx; i++){
    //     cout << symbolTable[i] << endl;
    // }
    return 0;
}