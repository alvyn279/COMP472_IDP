# COMP472
Artificial Intelligence - Indonesian Dot Puzzle

Duy-Khoi Le - 40026393

GitHub repo (please email me at alvyn279@gmail.com for access to this private repo): https://github.com/alvyn279/COMP472_IDP

## Indonesian Dot Puzzle

### Deliverables
Please find the project report and expectations of originality under `docs/`

### Search algorithms

- Limited depth-first search (DFS)
- Best-first search (BFS)
- Algorithm A*

### Running the project
Input is currently hardcoded in main execution file. This will be improved in next iteration.
There are also no dependencies to install.

From a terminal,
```sh
# move to root dir of project

mkdir output/

python main.py
```

#### Output

In `output` directory,

```
[puzzle_num]_[algo]_solutions.txt
[puzzle_num]_[algo]_search.txt
```

#### Dependencies/References

This project uses a customized priority queue implementation by Edward L Platt. [Here](https://github.com/elplatt/python-priorityq) is the library's repository.
