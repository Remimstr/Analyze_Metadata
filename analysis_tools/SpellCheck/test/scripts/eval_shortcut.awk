# eval_shortcut.awk: Saves time in evaluating whether spellcheck
# performed or not. Use as: awk -f eval_shortcut.awk infile > outfile
# Note the input files need to conform exactly to specification:
# Column #1 must be the original string
# Column #2 must be the mutated string of interest
# Column #3 must be the spellchecked string
# Column #4 is ignored

# Set the input and output delimiters to be a comma
BEGIN {
 FS = ","
 OFS = ","
}

# Replace all bad newline characters
{sub(/\r$/,"")}

# Print out the new headers (Correctly Spellchecked at $5)
NR==1 {print $0 ",Correctly Spellchecked?,Comments"}

## Get the first character of columns 1 and 3

# For each line evaluate criteria and print out information accordingly
{if (NR!=1)
 {if ($1 == $3)
    $5 = "Yes";
  else if ($1 == $2)
    $5 =  "-";
  else
    $5 = "No";
    {if (substr($1, 1, 1) != substr($2, 1, 1))
        $6 = "First character mismatch"}
  print $0}
 }
