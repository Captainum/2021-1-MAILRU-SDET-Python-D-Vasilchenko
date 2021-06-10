#!/bin/bash

pytest -s -l -v "${TESTS_PATH}" -n "${THREADS:-1}" --selenoid --alluredir "${ALLURE_PATH}"