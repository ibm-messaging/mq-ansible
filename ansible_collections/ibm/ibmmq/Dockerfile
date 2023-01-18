FROM ubuntu:20.04
# Requirements for connecting to Container (Via SSH):
RUN bash -c "apt-get update &> /dev/null && apt-get install -y openssh-server &> /dev/null && apt-get install -y locales &> /dev/null && apt-get install -y debconf &> /dev/null && apt install apt-utils &> /dev/null && apt-get install python3.6 &> /dev/null && apt install sudo &> /dev/null"
RUN mkdir /var/run/sshd
RUN echo 'root:g4QZB@vtjmw4vgjubh9' | chpasswd
# Edit ssh Configuration:
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN beforeLines="$(grep -B 1000 "#LoginGraceTime" /etc/ssh/sshd_config)" && afterLines="$(grep -A 1000 "#StrictModes" /etc/ssh/sshd_config)" && echo "$beforeLines""\nPermitRootLogin yes\n""$afterLines" >| /etc/ssh/sshd_config
RUN locale-gen en_US.UTF-8
RUN echo -e 'LANG="en_US.UTF-8"\nLANGUAGE="en_US:en"\n' > /etc/default/locale
# Define non-root user with sudo privileges
RUN useradd -d /home/tester -s /bin/bash -G sudo tester
RUN echo 'tester:4vgju@bh9g4QZBvtjmw' | chpasswd
RUN mkdir /home/tester
RUN chown tester /home/tester
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]