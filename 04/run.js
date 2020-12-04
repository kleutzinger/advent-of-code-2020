const fs = require("fs");
const _ = require("lodash");
const text = fs.readFileSync("input.txt", { encoding: "utf8", flag: "r" });
console.log(text);

text2 = text.split("\n");

console.log(text2);
required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];

let passports = [];
text2.forEach((e) => {});
