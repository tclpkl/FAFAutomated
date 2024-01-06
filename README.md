# FAF Automated Quantification of Retinal Degeneration

Developed by Timothy Lin

## About
This respository contains an early code prototype for an image-analysis algorithm quantifying deterioriation of FAF images that was hosted on a website via flask and GCP for testing purposes. I worked on this project to help support a medical research team's efforts at the USC Keck School of Medicine, aiming to help them more efficiently and accurately measure deterioration of retinal images and gauge treatment efficacy. Further developments were tested and a protocol paper is now pubslished under the Association for Research in Vision and Ophthalmology ([paper link](https://iovs.arvojournals.org/article.aspx?articleid=2787301)).

## Methodology
In designing the automated protocol, we identified an existing filter from Scikit-Image that works to isolate the bright features of an image. With FAF images, this filter helps identify non-hypopigmented spots since non-hypopigmented areas are brighter. We then only consider the non-bright sections that are considered potential hypopigmentation. In order to quantify the retinal deterioration, we continued to transform the filtered image until we could calculate the proportion of pixels in the processed FAF image that were dark. When applying the image filter to detect bright spots, there is also the h-value variable that controls the  threshold for detecting contrast in the original image. A smaller/higher h-value indicates more/less strictness in identifying bright spots, resulting in different sensitivities towards dark spots. We split the FAF image into two concentric layers to take advantage of this h-value variability. This sectioning aimed to reduce confounding from retinal vessels and shadows often on the outskirts of the image that would otherwise be incorrectly identifies as hypopigmentation. This layering allowed us to use different h-values to analyze the inner layer and the outer layer, where we are more lenient on identifying dark spots in the inner layer and less lenient on the outer layer. 

## Learned Skills
- Python
- Image Segmentation
- Flask
- GCP

## Future Steps
- Further refine algorithm and explore usage of AI/ML models on small datasets
