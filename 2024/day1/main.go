package main

import (
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func readInputFile(input_file string) ([]int, []int) {
	data, err := os.ReadFile(input_file)
	if err != nil {
		panic(err)
	}

	data_str := string(data)
	data_str = strings.Trim(data_str, "\n")
	lines := strings.Split(data_str, "\n")

	list1 := make([]int, 0)
	list2 := make([]int, 0)

	for _, line := range lines {
		items := strings.Split(line, "   ")
		t1, err := strconv.Atoi(items[0])
		if err != nil {
			panic(err)
		}

		t2, err := strconv.Atoi(items[1])
		if err != nil {
			panic(err)
		}

		list1 = append(list1, t1)
		list2 = append(list2, t2)
	}

	return list1, list2
}

func part1() int {
	l1, l2 := readInputFile("./input.txt")

	sort.Ints(l1)
	sort.Ints(l2)

	totalDist := 0
	for i := range len(l1) {
		dist := l1[i] - l2[i]
		totalDist += int(math.Abs(float64(dist)))
	}

	return totalDist
}

func part2() int {
	left, right := readInputFile("./input.txt")
	rightCount := map[int]int{}
	for _, n := range right {
		rightCount[n] += 1
	}

	totalSimilarityScore := 0
	for _, n := range left {
		count, exist := rightCount[n]
		if exist {
			totalSimilarityScore += (n * count)
		}
	}

	return totalSimilarityScore
}

func main() {
	res := part2()
	fmt.Println(res)
}
