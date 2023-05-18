from flask import Blueprint, render_template, request
import numpy as np
import pandas as pd
from website import db
from website import Movies
from fuzzywuzzy import process
import nltk
import pickle as pkl
import requests