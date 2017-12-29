#!/bin/sh

coverage run --source=app,utils -m pytest
coverage html -d coverage

