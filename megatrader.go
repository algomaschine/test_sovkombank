// Import necessary packages
package main

import (
	"fmt"
	"math"
	"sort"
	"sync"
)

type BondLot struct {
	Day      int
	Name     string
	Price    float64
	Quantity int
}

func (lot BondLot) Cost() float64 {
	return lot.Price * float64(lot.Quantity)
}

func (lot BondLot) Income() float64 {
	return float64(lot.Quantity) * (1 + 1000)
}

// Function to add bond lots
type BondLotList []BondLot

func AddBondLot(bondLots BondLotList, day int, name string, price float64, quantity int) BondLotList {
	return append(bondLots, BondLot{Day: day, Name: name, Price: price, Quantity: quantity})
}

// Function to maximize income
func MaximizeIncome(bondLots BondLotList, funds float64) (BondLotList, float64) {
	// Sort lots by day and then by price (ascending)
	sort.Slice(bondLots, func(i, j int) bool {
		if bondLots[i].Day == bondLots[j].Day {
			return bondLots[i].Price < bondLots[j].Price
		}
		return bondLots[i].Day < bondLots[j].Day
	})

	// Use WaitGroup to implement concurrency
	var wg sync.WaitGroup
	numWorkers := int(math.Min(float64(len(bondLots)), float64(4)))
	chunkSize := (len(bondLots) + numWorkers - 1) / numWorkers
	mutex := &sync.Mutex{}
	var purchasedLots BondLotList

	for i := 0; i < numWorkers; i++ {
		start := i * chunkSize
		end := (i + 1) * chunkSize
		if end > len(bondLots) {
			end = len(bondLots)
		}
		wg.Add(1)
		go func(lots BondLotList) {
			defer wg.Done()
			localFunds := funds
			localPurchased := BondLotList{}
			for _, lot := range lots {
				if lot.Cost() <= localFunds {
					localFunds -= lot.Cost()
					localPurchased = append(localPurchased, lot)
				}
			}
			mutex.Lock()
			if localFunds < funds {
				funds = localFunds
			}
			purchasedLots = append(purchasedLots, localPurchased...)
			mutex.Unlock()
		}(bondLots[start:end])
	}
	wg.Wait()

	return purchasedLots, funds
}

// Function to calculate total income
func CalculateTotalIncome(purchasedLots BondLotList) float64 {
	totalIncome := 0.0
	for _, lot := range purchasedLots {
		totalIncome += lot.Income()
	}
	return totalIncome
}

func main() {
	n := 2
	s := 8000.0
	bondLots := BondLotList{}
	bondLots = AddBondLot(bondLots, 1, "alfa-05", 100.2, 2)
	bondLots = AddBondLot(bondLots, 2, "alfa-05", 101.5, 5)
	bondLots = AddBondLot(bondLots, 2, "gazprom-17", 100.0, 2)

	purchasedLots, remainingFunds := MaximizeIncome(bondLots, s)

	// Print the total income
	totalIncome := CalculateTotalIncome(purchasedLots)
	fmt.Printf("Total income on day %d: %.2f\n", n+30, totalIncome)

	// Print the purchased lots
	for _, lot := range purchasedLots {
		fmt.Printf("%d %s %.2f %d\n", lot.Day, lot.Name, lot.Price, lot.Quantity)
	}

	fmt.Println("Remaining funds:", remainingFunds)
}
