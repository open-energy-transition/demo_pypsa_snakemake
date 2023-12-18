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

# docker run --name democontainer -v "$(pwd)"/input:/input -v "$(pwd)"/results:/results 

# sudo docker run -it --entrypoint /bin/bash demo-pypsa

# sudo docker run -it -v ~/prepared_networks:/prepared_networks --entrypoint /bin/bash demo-pypsa -c "snakemake --cores 1 prepare_networks"

# sudo rm -r results/
