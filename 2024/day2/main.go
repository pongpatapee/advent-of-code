package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func readInputFile(inputFile string) [][]int {
	data, err := os.ReadFile(inputFile)
	if err != nil {
		panic(err)
	}

	data_string := string(data)
	data_string = strings.Trim(data_string, "\n")

	reports := [][]int{}

	for _, s := range strings.Split(data_string, "\n") {
		report := []int{}

		for _, level := range strings.Split(s, " ") {
			n, err := strconv.Atoi(level)
			if err != nil {
				panic(err)
			}

			report = append(report, n)
		}

		reports = append(reports, report)
	}

	return reports
}

func safeDelta(a int, b int) bool {
	diff := a - b
	diff = int(math.Abs(float64(diff)))

	return diff >= 1 && diff <= 3
}

func isSafe(report []int, increasing bool) bool {
	for i := 0; i < len(report)-1; i++ {
		if increasing && report[i] >= report[i+1] {
			return false
		}

		if !increasing && report[i] <= report[i+1] {
			return false
		}

		if !safeDelta(report[i], report[i+1]) {
			return false
		}
	}

	return true
}

func part1() int {
	reports := readInputFile("./input.txt")

	numSafe := 0
	for _, report := range reports {
		if isSafe(report, true) || isSafe(report, false) {
			numSafe++
		}
	}

	return numSafe
}

func isSafePart2(report []int, increasing bool) bool {
	// TODO: finish part 2
	// numTolerable := 1

	for i := 0; i < len(report)-1; i++ {
		if increasing && report[i] >= report[i+1] {
			return false
		}

		if !increasing && report[i] <= report[i+1] {
			return false
		}

		if !safeDelta(report[i], report[i+1]) {
			return false
		}
	}

	return true
}

func part2() int {
	numSafe := 0

	return numSafe
}

func main() {
	res := part1()
	fmt.Println(res)
}
