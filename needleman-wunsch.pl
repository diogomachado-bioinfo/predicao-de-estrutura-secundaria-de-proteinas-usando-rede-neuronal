#!/usr/bin/env perl

# Needleman-Wunsch  Algorithm 
#https://github.com/sestaton/sesbio/blob/master/phylogenetics/needleman-wunsch.pl

# usage statement
#die "usage: $0 <sequence 1> <sequence 2>\n" unless @ARGV == 2;

# get sequences from command line
my ($file) = @ARGV;

open(my $fasta, "<", ("tmp/$file"));

$c = 0;
while (my $line = <$fasta> ) {
    chomp $line;    
    if ($line !~ />/ and $c == 0 and $line =~ /\w+/) {
        $seq1 = $line;
        $c++;
    }
    elsif ($line !~ />/ and $c == 1 and $line =~ /\w+/) {
        $seq2 = $line;
    }
}

close($fasta);

# scoring scheme
my $MATCH    =  1; # +1 for letters that match
my $MISMATCH = -1; # -1 for letters that mismatch
my $GAP      = -2737; # -1 for any gap
my $GAP_E      = -1157; # -1 for any gap

my %matrix = (
    "CC" => "351",
    "CE" => "-460",
    "CH" => "-557",
    "EE" => "2374",
    "EH" => "-2478",
    "HH" => "1796",
    "EC" => "-460",
    "HC" => "-557",
    "HE" => "-2478"
);

# initialization
my @matrix;
$matrix[0][0]{score}   = 0;
$matrix[0][0]{pointer} = "none";
for (my $j = 1; $j <= length($seq1); $j++) {
    $matrix[0][$j]{score}   = $GAP * $j;
    $matrix[0][$j]{pointer} = "left";
}
for (my $i = 1; $i <= length($seq2); $i++) {
    $matrix[$i][0]{score}   = $GAP * $i;
    $matrix[$i][0]{pointer} = "up";
}

# fill
for (my $i = 1; $i <= length($seq2); $i++) {
    for (my $j = 1; $j <= length($seq1); $j++) {
        my ($diagonal_score, $left_score, $up_score);

        # calculate match score
        my $letter1 = substr($seq1, $j-1, 1);
        my $letter2 = substr($seq2, $i-1, 1);   

        $diagonal_score = $matrix[$i-1][$j-1]{score} + $matrix{$letter1.$letter2};
=cut        
        if ($letter1 eq $letter2) {
            $diagonal_score = $matrix[$i-1][$j-1]{score} + $MATCH;
        }
        else {
            $diagonal_score = $matrix[$i-1][$j-1]{score} + $MISMATCH;
        }
=cut  
        # calculate gap scores
        if ($gapextend == 1) {
            $up_score   = $matrix[$i-1][$j]{score} + $GAP_E;
            $left_score = $matrix[$i][$j-1]{score} + $GAP_E;
        } else {
            $up_score   = $matrix[$i-1][$j]{score} + $GAP;
            $left_score = $matrix[$i][$j-1]{score} + $GAP;
        }
        
        # choose best score
        if ($diagonal_score >= $up_score) {
            if ($diagonal_score >= $left_score) {
                $matrix[$i][$j]{score}   = $diagonal_score;
                $matrix[$i][$j]{pointer} = "diagonal";
                $gapextend=0;
            }
	    else {
                $matrix[$i][$j]{score}   = $left_score;
                $matrix[$i][$j]{pointer} = "left";
                $gapextend=1;
            }
        } 
        else {
            if ($up_score >= $left_score) {
                $matrix[$i][$j]{score}   = $up_score;
                $matrix[$i][$j]{pointer} = "up";
                $gapextend=1;
            }
            else {
                $matrix[$i][$j]{score}   = $left_score;
                $matrix[$i][$j]{pointer} = "left";
                $gapextend=1;
            }
        }
    }
}

# trace-back

my $align1 = "";
my $align2 = "";

# start at last cell of matrix
my $j = length($seq1);
my $i = length($seq2);

while (1) {
    last if $matrix[$i][$j]{pointer} eq "none"; # ends at first cell of matrix

    if ($matrix[$i][$j]{pointer} eq "diagonal") {
        $align1 .= substr($seq1, $j-1, 1);
        $align2 .= substr($seq2, $i-1, 1);
        $i--;
        $j--;
    }
    elsif ($matrix[$i][$j]{pointer} eq "left") {
        $align1 .= substr($seq1, $j-1, 1);
        $align2 .= "-";
        $j--;
    }
    elsif ($matrix[$i][$j]{pointer} eq "up") {
        $align1 .= "-";
        $align2 .= substr($seq2, $i-1, 1);
        $i--;
    }    
}

$align1 = reverse $align1;
$align2 = reverse $align2;
print "$align1\n";
print "$align2\n";