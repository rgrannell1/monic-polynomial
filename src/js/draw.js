#!/usr/bin/env node

"use strict"





const doc = `
Usage:
	draw [-w WIDTH | --width WIDTH] [-h HEIGHT| --height HEIGHT]

Options:
	-w WIDTH, --width WIDTH    [default: 200]
	-h HEIGHT, --height HEIGHT [default: 200]
`






const docopt     = require('docopt').docopt
const nodeCanvas = require('canvas')
const fs         = require('fs')

const args       = docopt(doc)




const dimensions = {
	height: parseInt(args['--height'], 10),
	width:  parseInt(args['--width'], 10)
}

const canvas = new nodeCanvas(dimensions.width, dimensions.height)
const ctx    = canvas.getContext('2d')





for (let ith = 0; ith < dimensions.width; ++ith) {
	for (let jth = 0; jth < dimensions.width; ++jth) {

		ctx.fillStyle = Math.random( ) >= (1 / 2) ? "black" : "white"
		ctx.fillRect(ith, jth, 1, 1)

	}
}

ctx.save( )

canvas.createPNGStream( )
.on('data', chunk => {
	process.stdout.write(chunk)
})
