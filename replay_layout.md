Based off: https://github.com/dnunez02/rnd_reader/blob/master/reader.c#L16-L72

Other Notes:
The first 7 bytes are not input data.
Input data starts on the 8th byte with Player 1 then Player 2.

Format is as follows
| 08 | FF | FF | FF |
| -- | -- | -- | -- |

move byte (0x08) | 3 button bytes (0xFF 0xFF 0xFF)

`08 FF FF FF` is pure neutral, no hands on controller.


```
LP Press:   3F FC FF ==> 0011 1111 X 1111 1100 X 1111 1111
MP Press:   CF FC FF ==> 1100 1111 X 1111 1100 X 1111 1111
HP Press:   F3 FC FF ==> 1111 0011 X 1111 1100 X 1111 1111
LK Press:   FC F3 FF ==> 1111 1100 X 1111 0011 X 1111 1111
MK Press:   FF 33 FF ==> 1111 1111 X 0011 0011 X 1111 1111
HK Press:   FF C3 FF ==> 1111 1111 X 1100 0011 X 1111 1111
```
```
LP Hold:    BF FE FF ==> 1011 1111 X 1111 1110 X 1111 1111
MP Hold:    EF FE FF ==> 1110 1111 X 1111 1110 X 1111 1111
HP Hold:    FB FE FF ==> 1111 1011 X 1111 1110 X 1111 1111
LK Hold:    FE FB FF ==> 1111 1110 X 1111 1011 X 1111 1111
MK Hold:    FF BB FF ==> 1111 1111 X 1011 1011 X 1111 1111
HK Hold:    FF EB FF ==> 1111 1111 X 1110 1011 X 1111 1111
```
```
LP Release: 7F FD FF ==> 0111 1111 X 1111 1101 X 1111 1111
MP Release: DF FD FF ==> 1101 1111 X 1111 1101 X 1111 1111
HP Release: F7 FD FF ==> 1111 0111 X 1111 1101 X 1111 1111
LK Release: FD F7 FF ==> 1111 1101 X 1111 0111 X 1111 1111
MK Release: FF 77 FF ==> 1111 1111 X 0111 0111 X 1111 1111
HK Release: FF D7 FF ==> 1111 1111 X 1101 0111 X 1111 1111
```


Normal double button presses are the bitwise-and of the two buttons and
the actions done at that time.
Note that button A can be pressed while B is held. So we get
(B hold) & (A Press)


Biggest Example is Throw

```
LP+LK Press:   3C F0 FF ==> 0011 1100 X 1111 0000 X 1111 1111
LP+LK Hold:    BE FA FF ==> 1011 1110 X 1111 1010 X 1111 1111
LP+LK Release: 7D F5 FF ==> 0111 1101 X 1111 0101 X 1111 1111
```

Here is an exception to the rule
Dash does not register without that change in the last word

The third button byte is used to specify press/hold/release (`00`/`10`/`01`)
```
LP+MP Press:   0F FC CF ==> 0000 1111 X 1111 1100 X 1100 1111
LP+MP Hold:    AF FE EF ==> 1010 1111 X 1111 1110 X 1110 1111
LP+HP Release: 5F FD DF ==> 0101 1111 X 1111 1101 X 1101 1111
```

The same pattern is used with kicks to specify press/hold/release (`00`/`10`/`01`) in the third byte
```
LK+MK Press:   FC 33 3F ==> 1111 1100 X 0011 0011 X 0011 1111
LK+MK Hold:    FE BB BF ==> 1111 1110 X 1011 1011 X 1011 1111
LK+MK Release: FD 77 7F ==> 1111 1101 X 0111 0111 X 0111 1111
```

Snaps and assist calls do not seem to use that last word