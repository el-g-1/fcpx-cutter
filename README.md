# FCPX-file-cutter

This is an application that manipulates Final Cut Pro X
project files. Based on the input timestamps,
it slices video lanes.
The input timestamps must be acquired from some other
application.

## Usage

The application requires two files: the input XML file
and the txt file with timestamps in /30000s, one per line.
```
python FCPX_cutter.py [-h] --input_file INPUT_FILE --cuts_timestamps CUTS_TIMESTAMPS
```

## Dependencies

* Python >=3.0

