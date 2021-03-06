# head_hunter

Object localization (basic face localization) with PyTorch.


## Manual Labeling

In attempting to build a face localizer, we'll first manually label a reasonable number of images and see how training on a small dataset performs before deciding whether to proceed. To speed up labeling, we'll use a [Flask web app](https://github.com/dliedtka/head_hunter/tree/main/labeling).


## Face Localization

May want to do some data transforms since we only have about 3,000 images.


## Eventual Workflow

1. Scrape images for dataset, see [selfie_scraper repo](https://github.com/dliedtka/selfie_scraper).
2. Crop images to just faces (THIS REPO).
    - Try to implement on own with CNN object localization. This will require making images squares and then resizing to the same resolution.
    - Could look for existing face localization implementations.
3. Implement gender classifier and age prediction CNNs (FUTURE REPO).
    - Will need to again square and resize face images to same resolution.
    - Will age prediction work better with classification age buckets or as a regression problem?
