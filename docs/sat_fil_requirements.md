Saturation Filter requirements
===============================

----

## Saturation Filter

- I/O ports:
  - `clk`         (1 bit)
  - `rst`         (1 bit)
  - `in_data`     ('DATA_W' bits)
  - `in_valid`    (1 bit)
  - `out_data`    ('DATA_W' bits)
  - `out_valid`   (1 bit)
  - `ovf`         (1 bit)

- Parameters:
  - `THRESHOLD`: Sets the threshold value of the filter. Integer value. (default=8)
  - `DATA_W`: Sets the bit size of the input data. Integer value. (default=4bits)

----

- Clock (`clk`) frequency 5ns.

- Reset (`rst`):
  - Is synchronous.
  - Active HIGH.

- Input data (`in_data`):
  - Data width must be parameterized (`DATA_W`).
  - Integer value.

- Output data (`out_data`):
  - Integer value.

----

- Operation:
  - When `rst==1`, `out_data=0`, `out_valid=0`, `ovf=0`.
  - If `in_valid==0`, `out_data` keep the previous value and `in_data` will not be sampled.
  - If `in_valid==1`, `in_data` is sampled.
  - After `in_data` sampled, `out_data` will be available in the next clock cycle, by the following rules (for `in_valid=1`):

    |                       |                        |                |           |
    |:---------------------:|:----------------------:|:--------------:|:---------:|
    | `in_data > THRESHOLD` | `out_data = THRESHOLD` | `out_valid = 1`| `ovf = 1` |
    | `in_data =< THRESHOLD`| `out_data = in_data`   | `out_valid = 1`| `ovf = 0` |
    | `in_data = X`         | `out_data = X`         | `out_valid = 0`| `ovf = 0` |

----

<!-- SSDT UVC for Simple SyoSil Data Protocol. -->