FROM condaforge/mambaforge

RUN conda update -n base conda
RUN conda install -n base conda-libmamba-solver
RUN conda config --set solver libmamba

COPY . .

RUN conda env create -f env.yaml

RUN echo "source activate demo-pypsa" > ~/.bashrc
ENV PATH /opt/conda/envs/demo-pypsa/bin:$PATH

ENTRYPOINT [ "snakemake","--cores","1","calculate_sum" ]

# docker build -t demo-pypsa .

# docker run --name democontainer -v "$(pwd)"/input:/input -v "$(pwd)"/results:/results --rm demo_pypsa

# sudo rm -r results/