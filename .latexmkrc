#!/usr/bin/env perl

# $latex='uplatex %O -synctex=1 -interaction=nonstopmode %S';
$latex            = 'platex -synctex=1 -halt-on-error';
$pdflatex         = 'pdflatex %O -synctex=1 -interaction=nonstopmode %S';
$lualatex         = 'lualatex %O -synctex=1 -interaction=nonstopmode %S';
$xelatex          = 'xelatex %O -no-pdf -synctex=1 -shell-escape -interaction=nonstopmode %S';
$bibtex           = 'pbibtex';
# $biber           = 'biber  -u -U --output_safechars';
$biber            = 'biber %O --bblencoding=utf8 -u -U --output_safechars %B';
# $bibtex          = 'upbibtex %O %B';
# $makeindex       = 'upmendex %O -o %D %S';
$dvipdf           = 'dvipdfmx %O -o %D %S';
$dvips            = 'dvips %O -z -f %S | convbkmk -u > %D';
$ps2pdf           = 'ps2pdf %O %S %D';
$makeindex        = 'mendex %O -o %D %S';
$max_repeat       = 5;
$pdf_mode         = 3;
$pvc_view_file_via_temporary = 0;

if ($^O eq 'darwin') {
    $pvc_view_file_via_temporary=0;
    $pdf_previewer='open -ga /Applications/Preview.app';
} else {
    $pdf_previewer='xdg-open';
}
