all-python-file=$(shell find -name "*.py")
all:
	@for file in $(all-python-file); do \
		echo $$file "executed";   \
		python $$file; \
	done

