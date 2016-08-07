
package main

import(
	"bufio"
)



func readLines ( ) {

	scanner := bufio.NewScanner(fpath)

	for scanner.Scan( ) {
		jobs <- scanner.Text( )
	}

	close(jobs)

}

go func ( ) {

	wg.Wait( )
	close

}( )
