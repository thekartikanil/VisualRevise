from pygments.style import Style
from pygments.token import Token, Comment, Keyword, Name, String, Number, Operator, Punctuation, Literal

class CustomCodeStyle(Style):
    background_color = "#f2e5f5"
    styles = {
        Token: "#101010",
        Comment: "#365E32",
        Comment.Preproc: "#365E32",
        Keyword: "#ff4500",
        Name: "#0000ff",
        Name.Function: "#a020f0",
        Name.Class: "#a020f0",
        Name.Variable: "#0000ff",
        String: "#b22222",
        Number: "#b22222",
        Operator: "#ff4500",
        Punctuation: "#ff4500",
        Literal: "#b22222",
    }
