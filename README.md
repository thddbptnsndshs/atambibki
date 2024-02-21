# А там бибки!

A bibliography management tool for biblatex, built with Python and MongoDB. Gather the scattered .bib reference files on your computer and construct a database so as to never copy and paste bib entries again.

## Usage

|  script           |  action |
|-------------------|---------|
|`atambibki -U`     |update the database|
|`atambibki -n filename`|write the missing entries in `filename.tex` to `ref.bib` in the same directory|

## Installation for MacOS

1. Install the [MongoDB Community Server](https://www.mongodb.com/try/download/community). Go by the [installation instruction](https://www.prisma.io/dataguide/mongodb/setting-up-a-local-mongodb-database) and start your server at localhost.

2. Clone this directory to your home directory:

`cd ~`<br>
`git clone git@github.com:thddbptnsndshs/atambibki.git`<br>

3. Move the atambibki file with a zsh script to `/usr/local/bin`:

`sudo cp ~/atambibki/atambibki /usr/local/bin/`<br>

4. Give the necessary access permissions to the script:

`cd /usr/local/bin` <br>
`sudo chmod -x atambibki`<br>
`sudo chmod 755 atambibki`<br>

5. Open the `~/.zshrc` file and append the following lines:

`atambibki() {`<br>
`bash ~/atambibki/atambibki $1 $2}`<br>

6. Restart your Terminal. You can use the script now. Yay!
