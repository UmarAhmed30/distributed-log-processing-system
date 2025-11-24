from pyflink.datastream import StreamExecutionEnvironment

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    ds = env.from_collection([1, 2, 3, 4, 5])
    ds.map(lambda x: f"Number: {x}").print()
    env.execute("test_flink_job")

if __name__ == "__main__":
    main()
