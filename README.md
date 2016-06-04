# polynomial

This repository includes code to solve and graph large numbers of polynomial roots. It also includes code to deploy a DigitalOcean VM to run this code, since this task can raise a laptop's temperature to lightly knee-scortching.

![alt text](examples/example-1.png "Monic Polynomial Graph")

## Background

This tool generates solutions to all polynomials of a fixed order, with coefficients in a certain integer range. After obtaining the complex solutions to these polynomials it plots their real / complex parts. The colour assigned to each root corresponds to the product of the polynomials coefficients.

## Requirements

- Ansible.
- A DigitalOcean account, with an SSH key set up.
- `security/digital-ocean-token`: Your digital-ocean access key.
- `security/ssh-id`: The internal ID assigned to your SSH key (e.q 12345).

## VM-Size

The VM deployment script creates a 2GiB RAM (20$ / month).

## Usage

```bash
make create-vm

make environment

make solve-polynomials

make draw-solutions

make fetch-images
```

Both `make solve-polynomials` and `make draw-solutions` run asyncronously, so Ansible will not wait for them to complete before exiting. These jobs are run as screen-sesssions; to re-attach them run:

```bash
screen -list
```

to find the launched sessions, and

```bash
screen -a <numeric-prefix>
```

to open the process. For the solution task you will see solution-rates and estimates of file-size / remaining time.

```
attempting to solve 104,060,401 polynomials. Do you want to start? [y/N]
rates:
    solved:                    70,000
    solved / second:           8,421

estimates:
    seconds remaining:         12,349
    estimated per hour:        30,315,600
    estimated file size:       28.41GiB
```

Press

<kbd>Ctrl + a</kbd>

<kbd>d</kbd>

to detach the screen session.

## Example Images

## License

The MIT License

Copyright (c) 2016 Ryan Grannell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Versioning

Versioning complies with the Semantic Versioning 2.0.0 standard.

http://semver.org/
