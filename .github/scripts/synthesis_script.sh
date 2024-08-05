# Fine, I'll write my own script...

set -e

echo '::group::Instalando Dependencias'

sudo apt update -y
sudo apt install -y git wget xz-utils

echo '::endgroup::'


echo '::group::Clonando Ejemplos de F4PGA' #Se clona el repositorio para utilizar el archivo "environment.yml" más actualizado

git clone https://github.com/chipsalliance/f4pga-examples
cd f4pga-examples

echo '::endgroup::'


echo '::group::Definiendo Variables de Entorno'

FPGA_FAM="${FPGA_FAM:=xc7}"
F4PGA_INSTALL_DIR="${F4PGA_INSTALL_DIR:=/usr/local}"

echo "FPGA_FAM: $FPGA_FAM"
echo "F4PGA_INSTALL_DIR: $F4PGA_INSTALL_DIR"

echo '::endgroup::'


echo '::group::Instalando Miniconda3'

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O conda_installer.sh
sudo bash conda_installer.sh -u -b -p $F4PGA_INSTALL_DIR/$FPGA_FAM/conda;
source "$F4PGA_INSTALL_DIR/$FPGA_FAM/conda/etc/profile.d/conda.sh";
conda env create -f $FPGA_FAM/environment.yml

echo '::endgroup::'


echo '::group::Instalando arch-defs'

case "$FPGA_FAM" in
  xc7)    PACKAGES='install-xc7 xc7a50t_test xc7a100t_test';;
  *)
    echo "Unknowd FPGA_FAM <${FPGA_FAM}>!"
    exit 1
esac

mkdir -p "$F4PGA_INSTALL_DIR/$FPGA_FAM"

F4PGA_TIMESTAMP='20220920-124259'
F4PGA_HASH='007d1c1'

for PKG in $PACKAGES; do
  wget -qO- https://storage.googleapis.com/symbiflow-arch-defs/artifacts/prod/foss-fpga-tools/symbiflow-arch-defs/continuous/install/${F4PGA_TIMESTAMP}/symbiflow-arch-defs-${PKG}-${F4PGA_HASH}.tar.xz | sudo tar -xJC $F4PGA_INSTALL_DIR/${FPGA_FAM}
done

echo '::endgroup::'


echo '::group::Sintetizando Módulo(s)'

source "${F4PGA_INSTALL_DIR}/${FPGA_FAM}/conda/etc/profile.d/conda.sh"
conda activate $FPGA_FAM
cd ..

flag_in=false

while getopts "abc" opt; do
  flag_in=true
  case $opt in
    a)
      cd ..
      symbiflow_synth -t mux_4_1 -v mux_4_1.sv -d artix7 -p xc7a35tcpg236-1
      ;;
    b)
      echo "Running command B"
      ;;
    c)
      echo "Running command C"
      ;;
    *)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if ! $flag_in; then
  make
fi

echo '::endgroup::'