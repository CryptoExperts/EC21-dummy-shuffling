# EC21-dummy-shuffling

This repository contains the supporting code for the paper

> [Dummy Shuffling against Algebraic Attacks in White-box Implementations](https://ia.cr/2021/290)

by Alex Biryukov and Aleksei Udovenko ([EUROCRYPT 2021](https://link.springer.com/chapter/10.1007%2F978-3-030-77886-6_8)).

Currently, it includes:

1. [Slides](./slides.pdf) of the presentation.
1. [Proof-of-concept](./poc_differential_attack_on_shuffling.py) of the differential algebraic attack on dummyless shuffling. (requires [SageMath](https://sagemath.org/))

## Information

Citation:

```bib
@InProceedings{EC:BirUdo21,
    author = "Biryukov, Alex and Udovenko, Aleksei",
    editor = "Canteaut, Anne and Standaert, Fran{\c{c}}ois-Xavier",
    title = "Dummy Shuffling Against Algebraic Attacks in White-Box Implementations",
    booktitle = "Advances in Cryptology -- EUROCRYPT 2021",
    year = "2021",
    publisher = "Springer International Publishing",
    address = "Cham",
    pages = "219--248",
    isbn = "978-3-030-77886-6"
}
```

**Author:** Aleksei Udovenko

**License:** GNU GPL v3