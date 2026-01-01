package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type SudokuRequest struct {
	Grid [][]int `json:"grid"`
}

func isValid(grid [][]int, row, col, num int) bool {
	for i := 0; i < 9; i++ {
		if grid[row][i] == num || grid[i][col] == num {
			return false
		}
	}

	startRow := row - row%3
	startCol := col - col%3

	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			if grid[startRow+i][startCol+j] == num {
				return false
			}
		}
	}
	return true
}

func solveSudoku(grid [][]int) bool {
	for row := 0; row < 9; row++ {
		for col := 0; col < 9; col++ {
			if grid[row][col] == 0 {
				for num := 1; num <= 9; num++ {
					if isValid(grid, row, col, num) {
						grid[row][col] = num
						if solveSudoku(grid) {
							return true
						}
						grid[row][col] = 0
					}
				}
				return false
			}
		}
	}
	return true
}

func solveHandler(w http.ResponseWriter, r *http.Request) {
	var req SudokuRequest
	json.NewDecoder(r.Body).Decode(&req)

	if solveSudoku(req.Grid) {
		json.NewEncoder(w).Encode(req.Grid)
	} else {
		http.Error(w, "No solution exists", http.StatusBadRequest)
	}
}

func main() {
	http.HandleFunc("/solve", solveHandler)
	log.Println("Sudoku Solver backend running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
